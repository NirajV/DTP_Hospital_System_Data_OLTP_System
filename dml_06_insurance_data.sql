-- Hospital OLTP System - Insurance Data (DML - Part 6)
-- Insurance Companies, Plans, and Patient Policies
--
-- This file contains insurance master data and patient policy assignments
-- 
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_06_insurance_data.sql

USE hospital_OLTP_system;

-- =====================================================
-- INSURANCE COMPANIES
-- =====================================================

-- INSERT INTO insurance_companies (company_name, company_code, phone, email, is_active) VALUES
-- ('Blue Cross Blue Shield', 'BCBS', '1-800-555-0001', 'claims@bcbs.com', TRUE),
-- ('UnitedHealthcare', 'UHC', '1-800-555-0002', 'claims@uhc.com', TRUE),
-- ('Aetna', 'AETNA', '1-800-555-0003', 'claims@aetna.com', TRUE),
-- ('Cigna', 'CIGNA', '1-800-555-0004', 'claims@cigna.com', TRUE);

-- =====================================================
-- INSURANCE PLANS
-- =====================================================

INSERT INTO insurance_plans (insurance_company_id, plan_name, plan_code, plan_type, coverage_level, deductible_amount, copay_amount, is_active) VALUES
(1, 'BCBS Premium PPO', 'PPO-PREM', 'PPO', 'family', 2000.00, 25.00, TRUE),
(1, 'BCBS Basic HMO', 'HMO-BASIC', 'HMO', 'individual', 1500.00, 20.00, TRUE),
(2, 'UHC Choice Plus', 'CHOICE-PLUS', 'PPO', 'family', 2500.00, 30.00, TRUE),
(3, 'Aetna Open Access', 'OPEN-ACCESS', 'PPO', 'individual', 1800.00, 25.00, TRUE);

-- =====================================================
-- PATIENT INSURANCE POLICIES
-- =====================================================

INSERT INTO patient_insurance_policies (patient_id, insurance_plan_id, policy_number, group_number, subscriber_name, subscriber_relationship, policy_start_date, is_primary, status) VALUES
(1, 1, 'BCBS-001-12345', 'GRP001', 'Alice Anderson', 'self', '2023-01-01', TRUE, 'active'),
(2, 3, 'UHC-002-54321', 'GRP002', 'Robert Taylor', 'self', '2023-01-01', TRUE, 'active'),
(3, 4, 'AETNA-003-98765', 'GRP003', 'Jennifer Martinez', 'self', '2023-01-01', TRUE, 'active');

COMMIT;

SELECT 'Insurance data (companies, plans, policies) loaded successfully!' AS status;
