-- Hospital OLTP System - Organizational Data (DML - Part 2)
-- Departments, Facilities, Rooms, and Beds
--
-- This file contains the organizational structure of the hospital
-- 
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_02_organizational_data.sql

USE hospital_OLTP_system;

-- =====================================================
-- 2. ORGANIZATIONAL DATA - DEPARTMENTS, FACILITIES, ROOMS, BEDS
-- =====================================================

-- =====================================================
-- DEPARTMENTS
-- =====================================================

-- INSERT INTO departments (department_name, department_code, location, phone, email, status) VALUES
-- ('Cardiology', 'CARD', 'Building A, Floor 3', '555-0101', 'cardiology@hospital.com', 'active'),
-- ('Neurology', 'NEUR', 'Building A, Floor 4', '555-0102', 'neurology@hospital.com', 'active'),
-- ('Pediatrics', 'PEDI', 'Building B, Floor 1', '555-0103', 'pediatrics@hospital.com', 'active'),
-- ('Orthopedics', 'ORTH', 'Building B, Floor 2', '555-0104', 'orthopedics@hospital.com', 'active'),
-- ('Emergency', 'EMER', 'Building C, Ground Floor', '555-0105', 'emergency@hospital.com', 'active'),
-- ('Radiology', 'RADI', 'Building A, Floor 1', '555-0106', 'radiology@hospital.com', 'active'),
-- ('General Medicine', 'GENM', 'Building A, Floor 2', '555-0107', 'general@hospital.com', 'active'),
-- ('Surgery', 'SURG', 'Building C, Floor 3', '555-0108', 'surgery@hospital.com', 'active'),
-- ('Oncology', 'ONCO', 'Building B, Floor 3', '555-0109', 'oncology@hospital.com', 'active'),
-- ('Pharmacy', 'PHAR', 'Building A, Ground Floor', '555-0110', 'pharmacy@hospital.com', 'active');

-- =====================================================
-- FACILITIES
-- =====================================================

INSERT INTO facilities (facility_name, facility_type, address, status) VALUES
('Main Hospital Building', 'building', '123 Medical Center Blvd', 'active'),
('West Wing', 'wing', '123 Medical Center Blvd', 'active'),
('East Wing', 'wing', '123 Medical Center Blvd', 'active'),
('Emergency Department', 'unit', '123 Medical Center Blvd', 'active');

-- =====================================================
-- ROOMS
-- =====================================================

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

-- =====================================================
-- BEDS
-- =====================================================

-- INSERT INTO beds (room_id, bed_number, bed_type, status) VALUES
-- (1, 'A', 'standard', 'available'),
-- (2, 'A', 'standard', 'available'),
-- (3, 'A', 'ICU', 'available'),
-- (4, 'A', 'pediatric', 'available'),
-- (5, 'A', 'standard', 'available'),
-- (6, 'A', 'standard', 'available'),
-- (7, 'A', 'standard', 'available');

COMMIT;

SELECT 'Organizational data (departments, facilities, rooms, beds) loaded successfully!' AS status;
