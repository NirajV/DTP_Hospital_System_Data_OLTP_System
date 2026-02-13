-- Hospital OLTP System - Patient Data (DML - Part 4)
-- Patients, Addresses, Emergency Contacts, and Appointments
--
-- This file contains patient demographic information and appointment scheduling
-- 
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_04_patient_data.sql

USE hospital_OLTP_system;

-- =====================================================
-- PATIENTS
-- =====================================================

-- INSERT INTO patients (mrn, first_name, last_name, date_of_birth, gender, ssn, phone, email, blood_group, marital_status, registration_date, status) VALUES
-- ('MRN001', 'Alice', 'Anderson', '1985-05-15', 'Female', '123-45-6001', '555-4001', 'alice.a@email.com', 'A+', 'married', '2023-01-15', 'active'),
-- ('MRN002', 'Robert', 'Taylor', '1990-08-22', 'Male', '123-45-6002', '555-4002', 'robert.t@email.com', 'B+', 'single', '2023-02-20', 'active'),
-- ('MRN003', 'Jennifer', 'Martinez', '1978-12-10', 'Female', '123-45-6003', '555-4003', 'jennifer.m@email.com', 'O+', 'married', '2023-03-10', 'active'),
-- ('MRN004', 'William', 'Garcia', '2015-03-30', 'Male', '123-45-6004', '555-4004', 'w.garcia@email.com', 'AB+', 'single', '2023-04-05', 'active'),
-- ('MRN005', 'Lisa', 'Rodriguez', '1995-06-18', 'Female', '123-45-6005', '555-4005', 'lisa.r@email.com', 'O-', 'single', '2023-05-12', 'active');

-- =====================================================
-- PATIENT ADDRESSES
-- =====================================================

-- INSERT INTO patient_addresses (patient_id, address_type, street_address1, city, state, postal_code, is_primary) VALUES
-- (1, 'home', '123 Main St', 'Springfield', 'IL', '62701', TRUE),
-- (2, 'home', '456 Oak Ave', 'Springfield', 'IL', '62702', TRUE),
-- (3, 'home', '789 Pine Rd', 'Springfield', 'IL', '62703', TRUE),
-- (4, 'home', '321 Elm St', 'Springfield', 'IL', '62704', TRUE),
-- (5, 'home', '654 Maple Dr', 'Springfield', 'IL', '62705', TRUE);

-- =====================================================
-- PATIENT EMERGENCY CONTACTS
-- =====================================================

-- INSERT INTO patient_emergency_contacts (patient_id, contact_name, relationship, phone, is_primary) VALUES
-- (1, 'Bob Anderson', 'Spouse', '555-4006', TRUE),
-- (2, 'Mary Taylor', 'Mother', '555-4007', TRUE),
-- (3, 'Carlos Martinez', 'Spouse', '555-4008', TRUE),
-- (4, 'Linda Garcia', 'Mother', '555-4009', TRUE),
-- (5, 'James Rodriguez', 'Brother', '555-4010', TRUE);

-- =====================================================
-- APPOINTMENT TYPES
-- =====================================================

-- INSERT INTO appointment_types (type_name, description, default_duration) VALUES
-- ('Initial Consultation', 'First visit with a new patient', 45),
-- ('Follow-up', 'Follow-up visit for existing condition', 30),
-- ('Annual Physical', 'Annual physical examination', 60),
-- ('Emergency', 'Emergency appointment', 30),
-- ('Procedure', 'Medical procedure appointment', 90);

-- =====================================================
-- APPOINTMENTS
-- =====================================================

-- INSERT INTO appointments (appointment_number, patient_id, doctor_id, appointment_type_id, appointment_date, appointment_time, duration_minutes, reason, status, priority) VALUES
-- ('APT001', 1, 1, 2, '2026-02-15', '10:00:00', 30, 'Regular cardiac checkup', 'confirmed', 'routine'),
-- ('APT002', 2, 2, 1, '2026-02-15', '11:00:00', 45, 'Headache consultation', 'scheduled', 'routine'),
-- ('APT003', 3, 3, 2, '2026-02-16', '09:00:00', 30, 'Child vaccination', 'confirmed', 'routine'),
-- ('APT004', 4, 4, 1, '2026-02-16', '14:00:00', 60, 'Knee pain evaluation', 'scheduled', 'routine'),
-- ('APT005', 5, 1, 2, '2026-02-17', '15:00:00', 30, 'Follow-up visit', 'scheduled', 'routine');

-- COMMIT;

-- SELECT 'Patient data (patients, addresses, emergency contacts, appointments) loaded successfully!' AS status;
