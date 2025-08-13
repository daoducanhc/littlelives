-- Create database
CREATE DATABASE IF NOT EXISTS littlelives;
USE littlelives;

-- invoices table
DROP TABLE IF EXISTS invoices;
CREATE TABLE invoices (
    id VARCHAR(50) PRIMARY KEY,
    centre_id VARCHAR(50),
    class_id VARCHAR(50),
    student_id VARCHAR(50),
    invoice_date DATE,
    total_amount DECIMAL(10,2)
);

INSERT INTO invoices (id, centre_id, class_id, student_id, invoice_date, total_amount) VALUES
('inv_001', 'c_01', 'cls_01', 'stu_001', '2025-05-01', 300.00),
('inv_002', 'c_01', 'cls_02', 'stu_002', '2025-06-01', 200.00),
('inv_003', 'c_02', 'cls_01', 'stu_003', '2025-01-01', 500.00),
('inv_004', 'c_03', 'cls_03', 'stu_004', '2024-12-15', 400.00),
('inv_005', 'c_01', 'cls_01', 'stu_005', '2025-02-01', 150.00),
('inv_006', 'c_02', 'cls_02', 'stu_006', '2025-04-10', 250.00),
('inv_007', 'c_03', 'cls_01', 'stu_007', '2025-03-20', 300.00),
('inv_008', 'c_01', 'cls_02', 'stu_008', '2025-06-20', 100.00);

-- credit_notes table
DROP TABLE IF EXISTS credit_notes;
CREATE TABLE credit_notes (
    id VARCHAR(50) PRIMARY KEY,
    centre_id VARCHAR(50),
    class_id VARCHAR(50),
    student_id VARCHAR(50),
    credit_note_date DATE,
    total_amount DECIMAL(10,2)
);

INSERT INTO credit_notes (id, centre_id, class_id, student_id, credit_note_date, total_amount) VALUES
('cr_001', 'c_01', 'cls_01', 'stu_001', '2025-05-15', 100.00),
('cr_002', 'c_02', 'cls_02', 'stu_002', '2025-03-10', 50.00),
('cr_003', 'c_02', 'cls_03', 'stu_003', '2024-12-01', 300.00),
('cr_004', 'c_01', 'cls_01', 'stu_004', '2025-01-20', 120.00),
('cr_005', 'c_03', 'cls_02', 'stu_005', '2025-06-01', 200.00),
('cr_006', 'c_03', 'cls_03', 'stu_006', '2025-02-28', 80.00),
('cr_007', 'c_02', 'cls_01', 'stu_007', '2025-05-05', 110.00),
('cr_008', 'c_01', 'cls_02', 'stu_008', '2025-04-25', 90.00);

-- payments table
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50),
    document_type ENUM('invoice', 'credit_note'),
    amount_paid DECIMAL(10,2),
    payment_date DATE
);

INSERT INTO payments (id, document_id, document_type, amount_paid, payment_date) VALUES
('pay_001', 'inv_001', 'invoice', 150.00, '2025-05-10'),
('pay_002', 'cr_003', 'credit_note', 100.00, '2025-02-01'),
('pay_003', 'inv_002', 'invoice', 200.00, '2025-06-10'),
('pay_004', 'inv_004', 'invoice', 100.00, '2025-01-10'),
('pay_005', 'cr_006', 'credit_note', 40.00, '2025-03-05'),
('pay_006', 'inv_006', 'invoice', 250.00, '2025-05-01'),
('pay_007', 'cr_008', 'credit_note', 90.00, '2025-05-10'),
('pay_008', 'inv_005', 'invoice', 50.00, '2025-03-01');

-- fact table
DROP TABLE IF EXISTS ageing_fact;
CREATE TABLE ageing_fact (
    centre_id VARCHAR(50),
    class_id VARCHAR(50),
    document_id VARCHAR(50),
    document_date DATE,
    student_id VARCHAR(50),
    day_30 DECIMAL(10,2) DEFAULT 0.00,
    day_60 DECIMAL(10,2) DEFAULT 0.00,
    day_90 DECIMAL(10,2) DEFAULT 0.00,
    day_120 DECIMAL(10,2) DEFAULT 0.00,
    day_150 DECIMAL(10,2) DEFAULT 0.00,
    day_180 DECIMAL(10,2) DEFAULT 0.00,
    day_180_and_above DECIMAL(10,2) DEFAULT 0.00,
    document_type ENUM('invoice', 'credit_note'),
    as_at_date DATE
);
