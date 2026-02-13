-- Hospital OLTP System - Sample Data (DML)
-- This file contains all INSERT statements for the hospital_OLTP_system database
-- Organized by domain/category for easy reference and management
-- 
-- Usage:
--   mysql -u root -p hospital_OLTP_system < hospital_sample_data.sql
--   OR
--   mysql> USE hospital_OLTP_system;
--   mysql> SOURCE hospital_sample_data.sql;

USE hospital_OLTP_system;

-- =====================================================
-- 1. REFERENCE DATA - ICD AND CPT CODES
-- =====================================================

-- Insert ICD codes (diagnosis codes)
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'I10', 'Essential (primary) hypertension', 'Circulatory'),
('ICD-10', 'E11.9', 'Type 2 diabetes mellitus without complications', 'Endocrine'),
('ICD-10', 'J45.909', 'Unspecified asthma, uncomplicated', 'Respiratory'),
('ICD-10', 'M79.3', 'Panniculitis, unspecified', 'Musculoskeletal'),
('ICD-10', 'R51', 'Headache', 'Symptoms'),
('ICD-10', 'J06.9', 'Acute upper respiratory infection, unspecified', 'Respiratory'),
('ICD-10', 'K21.9', 'Gastro-esophageal reflux disease without esophagitis', 'Digestive');

-- Insert CPT codes (procedure/service codes)
INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
('99213', 'Office/outpatient visit, established patient, 20-29 minutes', 'Evaluation and Management', 1.50),
('99214', 'Office/outpatient visit, established patient, 30-39 minutes', 'Evaluation and Management', 2.10),
('80053', 'Comprehensive metabolic panel', 'Laboratory', 0.75),
('85025', 'Complete blood count with differential', 'Laboratory', 0.50),
('71045', 'Chest X-ray, 2 views', 'Radiology', 1.20),
('93000', 'Electrocardiogram, routine ECG with at least 12 leads', 'Cardiology', 0.60);

-- =====================================================
-- 2. ORGANIZATIONAL DATA - DEPARTMENTS, FACILITIES, ROOMS, BEDS
-- =====================================================

-- Insert departments
INSERT INTO departments (department_name, department_code, location, phone, email, status) VALUES
('Cardiology', 'CARD', 'Building A, Floor 3', '555-0101', 'cardiology@hospital.com', 'active'),
('Neurology', 'NEUR', 'Building A, Floor 4', '555-0102', 'neurology@hospital.com', 'active'),
('Pediatrics', 'PEDI', 'Building B, Floor 1', '555-0103', 'pediatrics@hospital.com', 'active'),
('Orthopedics', 'ORTH', 'Building B, Floor 2', '555-0104', 'orthopedics@hospital.com', 'active'),
('Emergency', 'EMER', 'Building C, Ground Floor', '555-0105', 'emergency@hospital.com', 'active'),
('Radiology', 'RADI', 'Building A, Floor 1', '555-0106', 'radiology@hospital.com', 'active'),
('General Medicine', 'GENM', 'Building A, Floor 2', '555-0107', 'general@hospital.com', 'active'),
('Surgery', 'SURG', 'Building C, Floor 3', '555-0108', 'surgery@hospital.com', 'active'),
('Oncology', 'ONCO', 'Building B, Floor 3', '555-0109', 'oncology@hospital.com', 'active'),
('Pharmacy', 'PHAR', 'Building A, Ground Floor', '555-0110', 'pharmacy@hospital.com', 'active');

-- Insert facilities
INSERT INTO facilities (facility_name, facility_type, address, status) VALUES
('Main Hospital Building', 'building', '123 Medical Center Blvd', 'active'),
('West Wing', 'wing', '123 Medical Center Blvd', 'active'),
('East Wing', 'wing', '123 Medical Center Blvd', 'active'),
('Emergency Department', 'unit', '123 Medical Center Blvd', 'active');

-- Insert rooms
INSERT INTO rooms (facility_id, department_id, room_number, room_type, floor_number, status) VALUES
(1, 1, '301', 'patient', 3, 'available'),
(1, 1, '302', 'patient', 3, 'available'),
(1, 2, '401', 'patient', 4, 'available'),
(1, 3, '101', 'patient', 1, 'available'),
(1, 4, '201', 'patient', 2, 'available'),
(1, 5, 'ER-1', 'ER', 0, 'available'),
(1, 5, 'ER-2', 'ER', 0, 'available'),
(1, 7, '202', 'examination', 2, 'available'),
(1, 7, '203', 'examination', 2, 'available'),
(1, 8, 'OR-1', 'operating', 3, 'available');

-- Insert beds
INSERT INTO beds (room_id, bed_number, bed_type, status) VALUES
(1, 'A', 'standard', 'available'),
(2, 'A', 'standard', 'available'),
(3, 'A', 'ICU', 'available'),
(4, 'A', 'pediatric', 'available'),
(5, 'A', 'standard', 'available'),
(6, 'A', 'standard', 'available'),
(7, 'A', 'standard', 'available');

-- =====================================================
-- 3. STAFF DATA - DOCTORS, NURSES, AND GENERAL STAFF
-- =====================================================

-- Insert sample doctors
INSERT INTO doctors (employee_id, first_name, last_name, specialization, department_id, phone, email, license_number, npi_number, hire_date, consultation_fee, status) VALUES
('DOC001', 'John', 'Smith', 'Cardiologist', 1, '555-1001', 'j.smith@hospital.com', 'LIC-001', 'NPI1234567890', '2015-03-15', 250.00, 'active'),
('DOC002', 'Sarah', 'Johnson', 'Neurologist', 2, '555-1002', 's.johnson@hospital.com', 'LIC-002', 'NPI1234567891', '2016-07-20', 200.00, 'active'),
('DOC003', 'Michael', 'Williams', 'Pediatrician', 3, '555-1003', 'm.williams@hospital.com', 'LIC-003', 'NPI1234567892', '2017-01-10', 150.00, 'active'),
('DOC004', 'Emily', 'Brown', 'Orthopedic Surgeon', 4, '555-1004', 'e.brown@hospital.com', 'LIC-004', 'NPI1234567893', '2018-05-12', 300.00, 'active'),
('DOC005', 'David', 'Davis', 'Emergency Medicine', 5, '555-1005', 'd.davis@hospital.com', 'LIC-005', 'NPI1234567894', '2019-09-01', 200.00, 'active'),
('DOC006', 'Jennifer', 'Martinez', 'Radiologist', 6, '555-1006', 'j.martinez@hospital.com', 'LIC-006', 'NPI1234567895', '2018-11-15', 275.00, 'active'),
('DOC007', 'Robert', 'Garcia', 'General Practitioner', 7, '555-1007', 'r.garcia@hospital.com', 'LIC-007', 'NPI1234567896', '2016-04-20', 175.00, 'active');

-- Insert nurses
INSERT INTO nurses (employee_id, first_name, last_name, department_id, license_number, license_type, phone, email, hire_date, status) VALUES
('NUR001', 'Lisa', 'Anderson', 1, 'RN-001', 'RN', '555-2001', 'l.anderson@hospital.com', '2017-06-01', 'active'),
('NUR002', 'James', 'Taylor', 2, 'RN-002', 'RN', '555-2002', 'j.taylor@hospital.com', '2018-03-15', 'active'),
('NUR003', 'Maria', 'Rodriguez', 3, 'RN-003', 'RN', '555-2003', 'm.rodriguez@hospital.com', '2019-01-10', 'active'),
('NUR004', 'William', 'Lee', 5, 'RN-004', 'RN', '555-2004', 'w.lee@hospital.com', '2017-09-20', 'active');

-- Insert general staff (administrative, support, etc.)
INSERT INTO staff (employee_id, first_name, last_name, department_id, position, phone, email, hire_date, status) VALUES
('STF001', 'Amanda', 'Wilson', 10, 'Pharmacist', '555-3001', 'a.wilson@hospital.com', '2018-02-15', 'active'),
('STF002', 'Kevin', 'Moore', 7, 'Medical Assistant', '555-3002', 'k.moore@hospital.com', '2019-05-10', 'active'),
('STF003', 'Patricia', 'White', NULL, 'Receptionist', '555-3003', 'p.white@hospital.com', '2017-08-01', 'active');

-- =====================================================
-- 4. PATIENT DATA - PATIENTS, ADDRESSES, EMERGENCY CONTACTS
-- =====================================================

-- Insert sample patients
INSERT INTO patients (mrn, first_name, last_name, date_of_birth, gender, ssn, phone, email, blood_group, marital_status, registration_date, status) VALUES
('MRN001', 'Alice', 'Anderson', '1985-05-15', 'Female', '123-45-6001', '555-4001', 'alice.a@email.com', 'A+', 'married', '2023-01-15', 'active'),
('MRN002', 'Robert', 'Taylor', '1990-08-22', 'Male', '123-45-6002', '555-4002', 'robert.t@email.com', 'B+', 'single', '2023-02-20', 'active'),
('MRN003', 'Jennifer', 'Martinez', '1978-12-10', 'Female', '123-45-6003', '555-4003', 'jennifer.m@email.com', 'O+', 'married', '2023-03-10', 'active'),
('MRN004', 'William', 'Garcia', '2015-03-30', 'Male', '123-45-6004', '555-4004', 'w.garcia@email.com', 'AB+', 'single', '2023-04-05', 'active'),
('MRN005', 'Lisa', 'Rodriguez', '1995-06-18', 'Female', '123-45-6005', '555-4005', 'lisa.r@email.com', 'O-', 'single', '2023-05-12', 'active');

-- Insert patient addresses
INSERT INTO patient_addresses (patient_id, address_type, street_address1, city, state, postal_code, is_primary) VALUES
(1, 'home', '123 Main St', 'Springfield', 'IL', '62701', TRUE),
(2, 'home', '456 Oak Ave', 'Springfield', 'IL', '62702', TRUE),
(3, 'home', '789 Pine Rd', 'Springfield', 'IL', '62703', TRUE),
(4, 'home', '321 Elm St', 'Springfield', 'IL', '62704', TRUE),
(5, 'home', '654 Maple Dr', 'Springfield', 'IL', '62705', TRUE);

-- Insert patient emergency contacts
INSERT INTO patient_emergency_contacts (patient_id, contact_name, relationship, phone, is_primary) VALUES
(1, 'Bob Anderson', 'Spouse', '555-4006', TRUE),
(2, 'Mary Taylor', 'Mother', '555-4007', TRUE),
(3, 'Carlos Martinez', 'Spouse', '555-4008', TRUE),
(4, 'Linda Garcia', 'Mother', '555-4009', TRUE),
(5, 'James Rodriguez', 'Brother', '555-4010', TRUE);

-- =====================================================
-- 5. APPOINTMENTS AND SCHEDULING
-- =====================================================

-- Insert appointment types
INSERT INTO appointment_types (type_name, description, default_duration) VALUES
('Initial Consultation', 'First visit with a new patient', 45),
('Follow-up', 'Follow-up visit for existing condition', 30),
('Annual Physical', 'Annual physical examination', 60),
('Emergency', 'Emergency appointment', 30),
('Procedure', 'Medical procedure appointment', 90);

-- Insert sample appointments
INSERT INTO appointments (appointment_number, patient_id, doctor_id, appointment_type_id, appointment_date, appointment_time, duration_minutes, reason, status, priority) VALUES
('APT001', 1, 1, 2, '2026-02-15', '10:00:00', 30, 'Regular cardiac checkup', 'confirmed', 'routine'),
('APT002', 2, 2, 1, '2026-02-15', '11:00:00', 45, 'Headache consultation', 'scheduled', 'routine'),
('APT003', 3, 3, 2, '2026-02-16', '09:00:00', 30, 'Child vaccination', 'confirmed', 'routine'),
('APT004', 4, 4, 1, '2026-02-16', '14:00:00', 60, 'Knee pain evaluation', 'scheduled', 'routine'),
('APT005', 5, 1, 2, '2026-02-17', '15:00:00', 30, 'Follow-up visit', 'scheduled', 'routine');

-- =====================================================
-- 6. PHARMACY DATA - MEDICATIONS AND INVENTORY
-- =====================================================

-- Insert medications
INSERT INTO medications (medication_name, generic_name, drug_class, ndc_code, dosage_form, strength, manufacturer, requires_prescription, unit_price, status) VALUES
('Lisinopril', 'Lisinopril', 'ACE Inhibitor', '60505-2685-1', 'tablet', '10mg', 'Apotex Corp', TRUE, 12.50, 'active'),
('Metformin', 'Metformin HCl', 'Biguanide', '60505-0144-1', 'tablet', '500mg', 'Apotex Corp', TRUE, 8.75, 'active'),
('Amoxicillin', 'Amoxicillin', 'Penicillin Antibiotic', '60505-0229-1', 'capsule', '500mg', 'Teva Pharmaceuticals', TRUE, 15.00, 'active'),
('Ibuprofen', 'Ibuprofen', 'NSAID', '60505-0121-1', 'tablet', '200mg', 'Major Pharmaceuticals', FALSE, 5.50, 'active'),
('Prednisone', 'Prednisone', 'Corticosteroid', '60505-0455-1', 'tablet', '20mg', 'Roxane Labs', TRUE, 10.00, 'active');

-- Insert medication inventory
INSERT INTO medication_inventory (medication_id, lot_number, expiration_date, quantity_on_hand, reorder_level, location, status) VALUES
(1, 'LOT2024A', '2026-12-31', 500, 100, 'Pharmacy Main', 'available'),
(2, 'LOT2024B', '2027-06-30', 750, 150, 'Pharmacy Main', 'available'),
(3, 'LOT2024C', '2026-09-30', 300, 100, 'Pharmacy Main', 'available'),
(4, 'LOT2024D', '2027-03-31', 1000, 200, 'Pharmacy Main', 'available'),
(5, 'LOT2024E', '2026-11-30', 200, 50, 'Pharmacy Main', 'available');

-- =====================================================
-- 7. INSURANCE DATA - COMPANIES, PLANS, AND POLICIES
-- =====================================================

-- Insert insurance companies
INSERT INTO insurance_companies (company_name, company_code, phone, email, is_active) VALUES
('Blue Cross Blue Shield', 'BCBS', '1-800-555-0001', 'claims@bcbs.com', TRUE),
('UnitedHealthcare', 'UHC', '1-800-555-0002', 'claims@uhc.com', TRUE),
('Aetna', 'AETNA', '1-800-555-0003', 'claims@aetna.com', TRUE),
('Cigna', 'CIGNA', '1-800-555-0004', 'claims@cigna.com', TRUE);

-- Insert insurance plans
INSERT INTO insurance_plans (insurance_company_id, plan_name, plan_code, plan_type, coverage_level, deductible_amount, copay_amount, is_active) VALUES
(1, 'BCBS Premium PPO', 'PPO-PREM', 'PPO', 'family', 2000.00, 25.00, TRUE),
(1, 'BCBS Basic HMO', 'HMO-BASIC', 'HMO', 'individual', 1500.00, 20.00, TRUE),
(2, 'UHC Choice Plus', 'CHOICE-PLUS', 'PPO', 'family', 2500.00, 30.00, TRUE),
(3, 'Aetna Open Access', 'OPEN-ACCESS', 'PPO', 'individual', 1800.00, 25.00, TRUE);

-- Insert patient insurance policies
INSERT INTO patient_insurance_policies (patient_id, insurance_plan_id, policy_number, group_number, subscriber_name, subscriber_relationship, policy_start_date, is_primary, status) VALUES
(1, 1, 'BCBS-001-12345', 'GRP001', 'Alice Anderson', 'self', '2023-01-01', TRUE, 'active'),
(2, 3, 'UHC-002-54321', 'GRP002', 'Robert Taylor', 'self', '2023-01-01', TRUE, 'active'),
(3, 4, 'AETNA-003-98765', 'GRP003', 'Jennifer Martinez', 'self', '2023-01-01', TRUE, 'active');

-- =====================================================
-- SUCCESS CONFIRMATION
-- =====================================================

COMMIT;

SELECT 'Hospital OLTP System sample data loaded successfully!' AS status;
