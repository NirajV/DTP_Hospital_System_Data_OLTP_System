-- Hospital OLTP System - Reference Data (DML - Part 1)
-- ICD and CPT Codes (Diagnostic and Procedure Code Standards)
--
-- This file contains master data for medical coding standards
-- 
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_01_reference_data.sql

-- USE hospital_OLTP_system;

-- =====================================================
-- ICD CODES - Diagnosis Classification
-- =====================================================
-- ICD-10 codes are used to classify and bill for diagnoses

-- INSERT INTO icd_codes (icd_version, code, description, category) VALUES
-- ('ICD-10', 'I10', 'Essential (primary) hypertension', 'Circulatory'),
-- ('ICD-10', 'E11.9', 'Type 2 diabetes mellitus without complications', 'Endocrine'),
-- ('ICD-10', 'J45.909', 'Unspecified asthma, uncomplicated', 'Respiratory'),
-- ('ICD-10', 'M79.3', 'Panniculitis, unspecified', 'Musculoskeletal'),
-- ('ICD-10', 'R51', 'Headache', 'Symptoms'),
-- ('ICD-10', 'J06.9', 'Acute upper respiratory infection, unspecified', 'Respiratory'),
-- ('ICD-10', 'K21.9', 'Gastro-esophageal reflux disease without esophagitis', 'Digestive');

-- =====================================================
-- CPT CODES - Procedure and Service Classification
-- =====================================================
-- CPT codes are used to classify and bill for medical procedures and services

-- INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
-- ('99213', 'Office/outpatient visit, established patient, 20-29 minutes', 'Evaluation and Management', 1.50),
-- ('99214', 'Office/outpatient visit, established patient, 30-39 minutes', 'Evaluation and Management', 2.10),
-- ('80053', 'Comprehensive metabolic panel', 'Laboratory', 0.75),
-- ('85025', 'Complete blood count with differential', 'Laboratory', 0.50),
-- ('71045', 'Chest X-ray, 2 views', 'Radiology', 1.20),
-- ('93000', 'Electrocardiogram, routine ECG with at least 12 leads', 'Cardiology', 0.60);

-- COMMIT;

-- SELECT 'Reference data (ICD/CPT codes) loaded successfully!' AS status;
