import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from src.daily_generate_fact import daily_generate_fact

def test_case_1():
    # Mock data
    invoices = pd.DataFrame([
        {"id": 1, "centre_id": 10, "class_id": 101, "invoice_date": "2025-06-20",
         "student_id": 1001, "total_amount": 100}
    ])
    credit_notes = pd.DataFrame([], columns=["id", "centre_id", "class_id", "credit_note_date", "student_id", "total_amount"])
    payments = pd.DataFrame([
        {"document_id": 1, "document_type": "invoice", "payment_date": "2025-06-25", "amount_paid": 20}
    ])

    data_override = {
        "invoices": invoices,
        "credit_notes": credit_notes,
        "payments": payments
    }

    result = daily_generate_fact(
        data_override=data_override,
        as_at_date=datetime(2025, 7, 7)
    )

    # The outstanding should be 80 and in the 30-day bucket
    assert result.iloc[0]['day_30'] == 80
    assert all(result.iloc[0][['day_60','day_90','day_120','day_150','day_180','day_180_and_above']] == 0)

def test_case_2():
    invoices = pd.DataFrame([
        {"id": 2, "centre_id": 20, "class_id": 202, "invoice_date": "2025-01-01",
         "student_id": 2002, "total_amount": 200}
    ])
    credit_notes = pd.DataFrame([], columns=["id", "centre_id", "class_id", "credit_note_date", "student_id", "total_amount"])
    payments = pd.DataFrame([
        {"document_id": 2, "document_type": "invoice", "payment_date": "2025-01-10", "amount_paid": 50}
    ])

    data_override = {
        "invoices": invoices,
        "credit_notes": credit_notes,
        "payments": payments
    }

    result = daily_generate_fact(
        data_override=data_override,
        as_at_date=datetime(2025, 7, 7)
    )

    # Outstanding should be 150 and in the >180 days bucket
    assert result.iloc[0]['day_180_and_above'] == 150
    assert all(result.iloc[0][['day_30','day_60','day_90','day_120','day_150','day_180']] == 0)