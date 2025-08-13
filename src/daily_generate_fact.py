import pandas as pd
from sqlalchemy import create_engine
from datetime import date

def daily_generate_fact(db_config=None, as_at_date=None, data_override=None):

    # as_at_date = pd.to_datetime(as_at_date or date.today())
    
    # set to July 7th 2025 for testing purposes
    as_at_date = pd.to_datetime("2025-07-07")

    # 1. Load data

    if data_override:
        invoices_df = data_override['invoices']
        credit_notes_df = data_override['credit_notes']
        payments_df = data_override['payments']
    else:
        engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

        invoices_df = pd.read_sql("SELECT * FROM invoices", engine, parse_dates=['invoice_date'])
        credit_notes_df = pd.read_sql("SELECT * FROM credit_notes", engine, parse_dates=['credit_note_date'])
        payments_df = pd.read_sql("SELECT * FROM payments", engine, parse_dates=['payment_date'])

    # 2. Transform invoices
    invoices_df = invoices_df.rename(columns={
        'id': 'document_id',
        'invoice_date': 'document_date'
    })
    invoices_df['document_type'] = 'invoice'

    # 3. Transform credit notes
    credit_notes_df = credit_notes_df.rename(columns={
        'id': 'document_id',
        'credit_note_date': 'document_date'
    })
    credit_notes_df['document_type'] = 'credit_note'

    # 4. Combine
    docs = pd.concat([invoices_df, credit_notes_df], ignore_index=True)

    # 5. Aggregate payments
    payment_sum = payments_df.groupby(['document_id', 'document_type'], as_index=False)['amount_paid'].sum()

    # 6. Join
    docs = docs.merge(payment_sum, on=['document_id', 'document_type'], how='left')
    docs['amount_paid'] = docs['amount_paid'].fillna(0)
    docs['outstanding_amount'] = docs['total_amount'] - docs['amount_paid']

    # 7. Filter
    docs = docs[docs['outstanding_amount'] > 0].copy()

    # 8. Calculate days difference
    docs['days_diff'] = (as_at_date - pd.to_datetime(docs['document_date'])).dt.days

    # 9. Create bucket columns
    bucket_cols = ['day_30','day_60','day_90','day_120','day_150','day_180','day_180_and_above']
    for col in bucket_cols:
        docs[col] = 0.00

    # 10. Bucket logic
    docs.loc[docs['days_diff'] <= 30, 'day_30'] = docs['outstanding_amount']
    docs.loc[docs['days_diff'].between(31, 60), 'day_60'] = docs['outstanding_amount']
    docs.loc[docs['days_diff'].between(61, 90), 'day_90'] = docs['outstanding_amount']
    docs.loc[docs['days_diff'].between(91, 120), 'day_120'] = docs['outstanding_amount']
    docs.loc[docs['days_diff'].between(121, 150), 'day_150'] = docs['outstanding_amount']
    docs.loc[docs['days_diff'].between(151, 180), 'day_180'] = docs['outstanding_amount']
    docs.loc[docs['days_diff'] > 180, 'day_180_and_above'] = docs['outstanding_amount']

    # 11. Final selection
    final_df = docs[['centre_id', 'class_id', 'document_id', 'document_date', 'student_id'] +
                    bucket_cols + ['document_type']].copy()
    final_df['as_at_date'] = as_at_date

    if not data_override:
        # 12. Load into MySQL if not in test mode
        with engine.begin() as conn:
            # Remove today's snapshot
            conn.execute(
                "DELETE FROM ageing_fact WHERE as_at_date = %s",
                (as_at_date.date(),)
            )

            # Insert fresh data
            insert_query = """
                INSERT INTO ageing_fact
                (centre_id, class_id, document_id, document_date, student_id,
                day_30, day_60, day_90, day_120, day_150, day_180, day_180_and_above,
                document_type, as_at_date)
                VALUES (%s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s)
            """
            for _, row in final_df.iterrows():
                conn.execute(insert_query, tuple(row))

        print(f"Inserted {len(final_df)} records into ageing_fact for {as_at_date.date()}")

        # Export final_df to CSV for verification
        final_df.to_csv(f"data/ageing_fact_{as_at_date.date()}.csv", index=False)
    else:
        # Return the final DataFrame for testing purposes
        return final_df
    
if __name__ == "__main__":
    daily_generate_fact(
        db_config={
            'host': 'localhost',
            'user': 'root',
            'password': 'IPM2022',
            'database': 'littlelives'
        },
    )


