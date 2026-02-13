-- Hospital OLTP System - Pharmacy Data (DML - Part 5)
-- Medications and Medication Inventory
--
-- This file contains medication master data and inventory management
-- 
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_05_pharmacy_data.sql

USE hospital_OLTP_system;

-- =====================================================
-- MEDICATIONS
-- =====================================================

-- INSERT INTO medications (medication_name, generic_name, drug_class, ndc_code, dosage_form, strength, manufacturer, requires_prescription, unit_price, status) VALUES
-- ('Lisinopril', 'Lisinopril', 'ACE Inhibitor', '60505-2685-1', 'tablet', '10mg', 'Apotex Corp', TRUE, 12.50, 'active'),
-- ('Metformin', 'Metformin HCl', 'Biguanide', '60505-0144-1', 'tablet', '500mg', 'Apotex Corp', TRUE, 8.75, 'active'),
-- ('Amoxicillin', 'Amoxicillin', 'Penicillin Antibiotic', '60505-0229-1', 'capsule', '500mg', 'Teva Pharmaceuticals', TRUE, 15.00, 'active'),
-- ('Ibuprofen', 'Ibuprofen', 'NSAID', '60505-0121-1', 'tablet', '200mg', 'Major Pharmaceuticals', FALSE, 5.50, 'active'),
-- ('Prednisone', 'Prednisone', 'Corticosteroid', '60505-0455-1', 'tablet', '20mg', 'Roxane Labs', TRUE, 10.00, 'active');

-- =====================================================
-- MEDICATION INVENTORY
-- =====================================================

INSERT INTO medication_inventory (medication_id, lot_number, expiration_date, quantity_on_hand, reorder_level, location, status) VALUES
(1, 'LOT2024A', '2026-12-31', 500, 100, 'Pharmacy Main', 'available'),
(2, 'LOT2024B', '2027-06-30', 750, 150, 'Pharmacy Main', 'available'),
(3, 'LOT2024C', '2026-09-30', 300, 100, 'Pharmacy Main', 'available'),
(4, 'LOT2024D', '2027-03-31', 1000, 200, 'Pharmacy Main', 'available'),
(5, 'LOT2024E', '2026-11-30', 200, 50, 'Pharmacy Main', 'available');

COMMIT;

SELECT 'Pharmacy data (medications and inventory) loaded successfully!' AS status;
