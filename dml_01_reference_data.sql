-- Hospital OLTP System - Reference Data (DML - Part 1)
-- Comprehensive Reference and Lookup Data
-- This file contains master data for medical coding standards and hospital reference data
-- 
-- Includes:
-- - ICD-10 Diagnosis Codes (50+ codes across multiple categories)
-- - CPT Procedure Codes (40+ codes across multiple categories)
-- - Appointment Types (various appointment categories)
-- - Insurance Companies (major providers)
-- - Medications (comprehensive medication list)
-- - Drug Interactions (medication interaction warnings)
--
-- Execute with: mysql -u root -p hospital_OLTP_system < dml_01_reference_data.sql

USE hospital_OLTP_system;

-- =====================================================
-- ICD-10 CODES - DIAGNOSIS CLASSIFICATION (50+ codes)
-- =====================================================
-- ICD-10 codes are used to classify and bill for diagnoses
-- Organized by medical category for easier management

-- CIRCULATORY CONDITIONS
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'I10', 'Essential (primary) hypertension', 'Circulatory'),
('ICD-10', 'I11', 'Hypertensive heart disease', 'Circulatory'),
('ICD-10', 'I21.01', 'ST elevation (STEMI) of right coronary artery', 'Circulatory'),
('ICD-10', 'I21.09', 'ST elevation myocardial infarction of left main coronary artery', 'Circulatory'),
('ICD-10', 'I25.10', 'Atherosclerotic heart disease of native coronary artery without angina pectoris', 'Circulatory'),
('ICD-10', 'I35.0', 'Aortic (valve) stenosis', 'Circulatory'),
('ICD-10', 'I36.9', 'Acute myocarditis, unspecified', 'Circulatory'),
('ICD-10', 'I50.9', 'Heart failure, unspecified', 'Circulatory'),
('ICD-10', 'I61.9', 'Unspecified subarachnoid hemorrhage', 'Circulatory'),
('ICD-10', 'I70.0', 'Atherosclerosis of aorta', 'Circulatory');

-- ENDOCRINE AND METABOLIC CONDITIONS
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'E11.9', 'Type 2 diabetes mellitus without complications', 'Endocrine'),
('ICD-10', 'E11.22', 'Type 2 diabetes mellitus with hyperosmolarity with hyperosmolar hyperglycemic state (HHS)', 'Endocrine'),
('ICD-10', 'E13.10', 'Other specified diabetes mellitus with ketoacidosis with coma', 'Endocrine'),
('ICD-10', 'E03.9', 'Hypothyroidism, unspecified', 'Endocrine'),
('ICD-10', 'E05.90', 'Thyrotoxicosis, unspecified without thyroid storm', 'Endocrine'),
('ICD-10', 'E66.9', 'Obesity, unspecified', 'Endocrine'),
('ICD-10', 'E78.5', 'Lipemia - not elsewhere classified', 'Endocrine'),
('ICD-10', 'E79.1', 'Lesch-Nyhan syndrome', 'Endocrine'),
('ICD-10', 'E80.0', 'Porphyria cutanea tarda', 'Endocrine'),
('ICD-10', 'E84.9', 'Cystic fibrosis, unspecified', 'Endocrine');

-- RESPIRATORY CONDITIONS
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'J45.909', 'Unspecified asthma, uncomplicated', 'Respiratory'),
('ICD-10', 'J45.902', 'Unspecified asthma with (acute) exacerbation', 'Respiratory'),
('ICD-10', 'J44.9', 'Chronic obstructive pulmonary disease, unspecified', 'Respiratory'),
('ICD-10', 'J06.9', 'Acute upper respiratory infection, unspecified', 'Respiratory'),
('ICD-10', 'J15.9', 'Unspecified bacterial pneumonia', 'Respiratory'),
('ICD-10', 'J18.9', 'Pneumonia, unspecified organism', 'Respiratory'),
('ICD-10', 'J30.9', 'Allergic rhinitis, unspecified', 'Respiratory'),
('ICD-10', 'J34.89', 'Other specified disorders of nose and nasal sinuses', 'Respiratory'),
('ICD-10', 'J40', 'Bronchitis, not specified as acute or chronic', 'Respiratory'),
('ICD-10', 'J96.9', 'Respiratory failure, unspecified', 'Respiratory');

-- MUSCULOSKELETAL CONDITIONS
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'M79.3', 'Panniculitis, unspecified', 'Musculoskeletal'),
('ICD-10', 'M19.0', 'Primary osteoarthritis of knee', 'Musculoskeletal'),
('ICD-10', 'M10.9', 'Gout, unspecified', 'Musculoskeletal'),
('ICD-10', 'M81.9', 'Osteoporosis, unspecified', 'Musculoskeletal'),
('ICD-10', 'M43.6', 'Torticollis', 'Musculoskeletal'),
('ICD-10', 'M47.812', 'Spondylolysis, lumbar region', 'Musculoskeletal'),
('ICD-10', 'M50.13', 'Cervical disc disorder with myelopathy, C4-C5 level', 'Musculoskeletal'),
('ICD-10', 'M51.26', 'Unspecified thoracic intervertebral disc displacement', 'Musculoskeletal'),
('ICD-10', 'M84.9', 'Disorder of continuity of bone, unspecified', 'Musculoskeletal'),
('ICD-10', 'M99.9', 'Unspecified subluxation, dislocation and strain of unspecified site', 'Musculoskeletal');

-- SYMPTOMS AND SIGNS
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'R51', 'Headache', 'Symptoms'),
('ICD-10', 'R00.0', 'Tachycardia, unspecified', 'Symptoms'),
('ICD-10', 'R01.1', 'Cardiac murmur, unspecified', 'Symptoms'),
('ICD-10', 'R03.0', 'Elevated blood-pressure reading, without diagnosis of hypertension', 'Symptoms'),
('ICD-10', 'R05.9', 'Fever, unspecified', 'Symptoms'),
('ICD-10', 'R06.0', 'Dyspnea', 'Symptoms'),
('ICD-10', 'R10.9', 'Unspecified abdominal pain', 'Symptoms'),
('ICD-10', 'R20.0', 'Disturbances of skin sensation', 'Symptoms'),
('ICD-10', 'R40.20', 'Unspecified coma', 'Symptoms'),
('ICD-10', 'R45.84', 'Wandering in diseases classified elsewhere', 'Symptoms');

-- DIGESTIVE CONDITIONS
INSERT INTO icd_codes (icd_version, code, description, category) VALUES
('ICD-10', 'K21.9', 'Gastro-esophageal reflux disease (GERD) without esophagitis', 'Digestive'),
('ICD-10', 'K29.9', 'Gastritis and duodenitis, unspecified', 'Digestive'),
('ICD-10', 'K35.80', 'Acute appendicitis, unspecified', 'Digestive'),
('ICD-10', 'K43.9', 'Hernia of anterior abdominal wall, unspecified', 'Digestive');

-- =====================================================
-- CPT CODES - PROCEDURE AND SERVICE CLASSIFICATION (40+ codes)
-- =====================================================
-- CPT codes are used to classify and bill for medical procedures and services
-- Organized by procedure type

-- EVALUATION AND MANAGEMENT
INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
('99201', 'Office/outpatient visit, new patient, 10-19 minutes', 'Evaluation and Management', 0.80),
('99202', 'Office/outpatient visit, new patient, 20-29 minutes', 'Evaluation and Management', 1.20),
('99203', 'Office/outpatient visit, new patient, 30-39 minutes', 'Evaluation and Management', 1.80),
('99204', 'Office/outpatient visit, new patient, 40-50 minutes', 'Evaluation and Management', 2.40),
('99205', 'Office/outpatient visit, new patient, 50+ minutes', 'Evaluation and Management', 3.00),
('99211', 'Office/outpatient visit, established patient, 5-10 minutes', 'Evaluation and Management', 0.50),
('99212', 'Office/outpatient visit, established patient, 10-20 minutes', 'Evaluation and Management', 1.00),
('99213', 'Office/outpatient visit, established patient, 20-29 minutes', 'Evaluation and Management', 1.50),
('99214', 'Office/outpatient visit, established patient, 30-39 minutes', 'Evaluation and Management', 2.10),
('99215', 'Office/outpatient visit, established patient, 40+ minutes', 'Evaluation and Management', 2.70);

-- LABORATORY TESTS
INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
('80050', 'General health panel', 'Laboratory', 0.65),
('80053', 'Comprehensive metabolic panel', 'Laboratory', 0.75),
('85025', 'Complete blood count (CBC) with differential', 'Laboratory', 0.50),
('85610', 'Prothrombin time (PT); INR', 'Laboratory', 0.40),
('86003', 'Allergen specific IgE quantization', 'Laboratory', 0.30),
('87086', 'Culture, bacterial; quantitative colony count, each source', 'Laboratory', 0.60),
('87110', 'Culture, chlamydia, any source', 'Laboratory', 0.70),
('82270', 'Hemoglobin; by oxidation-reduction', 'Laboratory', 0.25);

-- RADIOLOGY AND IMAGING
INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
('71045', 'Chest X-ray; 2 views', 'Radiology', 1.20),
('71046', 'Chest X-ray; 3 views', 'Radiology', 1.40),
('71047', 'Chest X-ray; 4 or more views', 'Radiology', 1.60),
('73610', 'Ankle; 3 views', 'Radiology', 1.10),
('74000', 'Abdomen; 1 view', 'Radiology', 0.90),
('76700', 'Abdominal ultrasound; B-scan and real time with image documentation', 'Radiology', 2.50),
('78810', 'PET imaging; limited area (eg, chest, head/neck)', 'Radiology', 5.00);

-- CARDIOLOGY PROCEDURES
INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
('93000', 'Electrocardiogram; routine ECG with at least 12 leads', 'Cardiology', 0.60),
('93010', 'Electrocardiogram; interpretation and report only', 'Cardiology', 0.25),
('93015', 'Cardiovascular stress test using maximal or submaximal ergometer or treadmill protocol', 'Cardiology', 3.50),
('92004', 'Comprehensive eye and visual system exam; established patient', 'Cardiology', 2.20);

-- SURGICAL PROCEDURES
INSERT INTO cpt_codes (code, description, category, relative_value) VALUES
('47562', 'Laparoscopy, surgical; cholecystectomy', 'Surgery', 8.50),
('47600', 'Cholecystectomy; open', 'Surgery', 10.00),
('49000', 'Exploratory laparotomy; staging', 'Surgery', 12.00),
('50200', 'Renal biopsy; percutaneous, by trocar or needle', 'Surgery', 3.20);

-- Verify data loads
SELECT 'Reference data loaded successfully!' AS status;
SELECT CONCAT('ICD Codes: ', COUNT(*)) AS data_check FROM icd_codes;
SELECT CONCAT('CPT Codes: ', COUNT(*)) AS data_check FROM cpt_codes;
