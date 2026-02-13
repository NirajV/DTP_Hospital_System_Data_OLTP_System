-- Hospital OLTP System - Staff Data (DML - Part 3)
-- Doctors, Nurses, and General Staff
--
-- This file contains all healthcare professionals and support staff
-- 
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_03_staff_data.sql

USE hospital_OLTP_system;

-- =====================================================
-- DOCTORS
-- =====================================================

-- INSERT INTO doctors (employee_id, first_name, last_name, specialization, department_id, phone, email, license_number, npi_number, hire_date, consultation_fee, status) VALUES
-- ('DOC001', 'John', 'Smith', 'Cardiologist', 1, '555-1001', 'j.smith@hospital.com', 'LIC-001', 'NPI1234567890', '2015-03-15', 250.00, 'active'),
-- ('DOC002', 'Sarah', 'Johnson', 'Neurologist', 2, '555-1002', 's.johnson@hospital.com', 'LIC-002', 'NPI1234567891', '2016-07-20', 200.00, 'active'),
-- ('DOC003', 'Michael', 'Williams', 'Pediatrician', 3, '555-1003', 'm.williams@hospital.com', 'LIC-003', 'NPI1234567892', '2017-01-10', 150.00, 'active'),
-- ('DOC004', 'Emily', 'Brown', 'Orthopedic Surgeon', 4, '555-1004', 'e.brown@hospital.com', 'LIC-004', 'NPI1234567893', '2018-05-12', 300.00, 'active'),
-- ('DOC005', 'David', 'Davis', 'Emergency Medicine', 5, '555-1005', 'd.davis@hospital.com', 'LIC-005', 'NPI1234567894', '2019-09-01', 200.00, 'active'),
-- ('DOC006', 'Jennifer', 'Martinez', 'Radiologist', 6, '555-1006', 'j.martinez@hospital.com', 'LIC-006', 'NPI1234567895', '2018-11-15', 275.00, 'active'),
-- ('DOC007', 'Robert', 'Garcia', 'General Practitioner', 7, '555-1007', 'r.garcia@hospital.com', 'LIC-007', 'NPI1234567896', '2016-04-20', 175.00, 'active');

-- =====================================================
-- NURSES
-- =====================================================

-- INSERT INTO nurses (employee_id, first_name, last_name, department_id, license_number, license_type, phone, email, hire_date, status) VALUES
-- ('NUR001', 'Lisa', 'Anderson', 1, 'RN-001', 'RN', '555-2001', 'l.anderson@hospital.com', '2017-06-01', 'active'),
-- ('NUR002', 'James', 'Taylor', 2, 'RN-002', 'RN', '555-2002', 'j.taylor@hospital.com', '2018-03-15', 'active'),
-- ('NUR003', 'Maria', 'Rodriguez', 3, 'RN-003', 'RN', '555-2003', 'm.rodriguez@hospital.com', '2019-01-10', 'active'),
-- ('NUR004', 'William', 'Lee', 5, 'RN-004', 'RN', '555-2004', 'w.lee@hospital.com', '2017-09-20', 'active');

-- =====================================================
-- GENERAL STAFF (Administrative, Support, etc)
-- =====================================================

-- INSERT INTO staff (employee_id, first_name, last_name, department_id, position, phone, email, hire_date, status) VALUES
-- ('STF001', 'Amanda', 'Wilson', 10, 'Pharmacist', '555-3001', 'a.wilson@hospital.com', '2018-02-15', 'active'),
-- ('STF002', 'Kevin', 'Moore', 7, 'Medical Assistant', '555-3002', 'k.moore@hospital.com', '2019-05-10', 'active'),
-- ('STF003', 'Patricia', 'White', NULL, 'Receptionist', '555-3003', 'p.white@hospital.com', '2017-08-01', 'active');

-- COMMIT;

-- SELECT 'Staff data (doctors, nurses, general staff) loaded successfully!' AS status;
