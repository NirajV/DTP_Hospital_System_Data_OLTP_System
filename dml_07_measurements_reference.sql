-- =====================================================
-- Hospital OLTP System — Measurement Reference Seed
-- Implements Appendix C of Requirement.md
-- Depends on: create_schema_measurements.sql
-- =====================================================
-- Loads:
--   * measurement_units    — common clinical units (with UCUM codes)
--   * measurement_types    — vital signs + frequently used labs (with LOINC)
--
-- Idempotent: uses INSERT ... ON DUPLICATE KEY UPDATE so re-runs are safe.
-- Units are seeded first; types resolve default_unit_id by unit_code lookup.
-- =====================================================

USE hospital_OLTP_system;

-- -----------------------------------------------------
-- measurement_units
-- -----------------------------------------------------
INSERT INTO measurement_units (unit_code, unit_name, ucum_code) VALUES
    -- pressure
    ('mmHg',    'Millimeters of mercury',          'mm[Hg]'),
    -- temperature
    ('degF',    'Degrees Fahrenheit',              '[degF]'),
    ('degC',    'Degrees Celsius',                 'Cel'),
    -- rate / count
    ('bpm',     'Beats per minute',                '{beats}/min'),
    ('rpm',     'Respirations per minute',         '{breaths}/min'),
    ('count',   'Count',                           '1'),
    -- percentage / ratio
    ('pct',     'Percent',                         '%'),
    -- length
    ('in',      'Inches',                          '[in_i]'),
    ('cm',      'Centimeters',                     'cm'),
    -- mass
    ('lb',      'Pounds',                          '[lb_av]'),
    ('kg',      'Kilograms',                       'kg'),
    -- derived
    ('kg_m2',   'Kilograms per square meter',      'kg/m2'),
    -- pain scale
    ('score10', 'Score 0-10',                      '{score}'),
    -- lab concentrations
    ('g_dL',    'Grams per deciliter',             'g/dL'),
    ('mg_dL',   'Milligrams per deciliter',        'mg/dL'),
    ('mmol_L',  'Millimoles per liter',            'mmol/L'),
    ('mEq_L',   'Milliequivalents per liter',      'meq/L'),
    ('U_L',     'Units per liter',                 'U/L'),
    ('ng_mL',   'Nanograms per milliliter',        'ng/mL'),
    ('pg_mL',   'Picograms per milliliter',        'pg/mL'),
    ('K_uL',    'Thousand cells per microliter',   '10*3/uL'),
    ('M_uL',    'Million cells per microliter',    '10*6/uL'),
    ('fL',      'Femtoliters',                     'fL'),
    ('IU_mL',   'International units per mL',      '[IU]/mL'),
    -- qualitative
    ('qual',    'Qualitative result',              NULL)
ON DUPLICATE KEY UPDATE
    unit_name = VALUES(unit_name),
    ucum_code = VALUES(ucum_code);

-- -----------------------------------------------------
-- measurement_types — VITAL SIGNS
-- (matches columns in encounter_vitals so backfill can map 1:1)
-- -----------------------------------------------------
INSERT INTO measurement_types (type_code, type_name, category, loinc_code, default_unit_id, normal_range_low, normal_range_high)
SELECT * FROM (
    SELECT 'bp_systolic'        AS type_code, 'Blood Pressure (Systolic)'  AS type_name, 'vital_sign'      AS category, '8480-6'  AS loinc, 'mmHg'    AS unit, 90    AS lo, 130   AS hi UNION ALL
    SELECT 'bp_diastolic',            'Blood Pressure (Diastolic)',          'vital_sign',     '8462-4',         'mmHg',           60,        85 UNION ALL
    SELECT 'heart_rate',              'Heart Rate',                           'vital_sign',     '8867-4',         'bpm',            60,        100 UNION ALL
    SELECT 'respiratory_rate',        'Respiratory Rate',                     'vital_sign',     '9279-1',         'rpm',            12,        20 UNION ALL
    SELECT 'temperature_f',           'Body Temperature (Fahrenheit)',        'vital_sign',     '8331-1',         'degF',           97.0,      99.5 UNION ALL
    SELECT 'temperature_c',           'Body Temperature (Celsius)',           'vital_sign',     '8310-5',         'degC',           36.1,      37.5 UNION ALL
    SELECT 'oxygen_saturation',       'Oxygen Saturation (SpO2)',             'vital_sign',     '2708-6',         'pct',            95,        100 UNION ALL
    SELECT 'pain_score',              'Pain Score',                            'vital_sign',     '72514-3',        'score10',        0,         3
) AS v
JOIN measurement_units u ON u.unit_code = v.unit
ON DUPLICATE KEY UPDATE
    type_name         = VALUES(type_name),
    category          = VALUES(category),
    loinc_code        = VALUES(loinc_code),
    default_unit_id   = VALUES(default_unit_id),
    normal_range_low  = VALUES(normal_range_low),
    normal_range_high = VALUES(normal_range_high);

-- -----------------------------------------------------
-- measurement_types — ANTHROPOMETRIC
-- -----------------------------------------------------
INSERT INTO measurement_types (type_code, type_name, category, loinc_code, default_unit_id, normal_range_low, normal_range_high)
SELECT * FROM (
    SELECT 'weight_lb' AS type_code, 'Body Weight (lb)' AS type_name, 'anthropometric' AS category, '29463-7' AS loinc, 'lb' AS unit, NULL AS lo, NULL AS hi UNION ALL
    SELECT 'weight_kg',                 'Body Weight (kg)',           'anthropometric', '29463-7', 'kg',     NULL,   NULL UNION ALL
    SELECT 'height_in',                 'Body Height (in)',           'anthropometric', '8302-2',  'in',     NULL,   NULL UNION ALL
    SELECT 'height_cm',                 'Body Height (cm)',           'anthropometric', '8302-2',  'cm',     NULL,   NULL UNION ALL
    SELECT 'bmi',                       'Body Mass Index',             'anthropometric', '39156-5', 'kg_m2',  18.5,   24.9
) AS v
JOIN measurement_units u ON u.unit_code = v.unit
ON DUPLICATE KEY UPDATE
    type_name         = VALUES(type_name),
    category          = VALUES(category),
    loinc_code        = VALUES(loinc_code),
    default_unit_id   = VALUES(default_unit_id),
    normal_range_low  = VALUES(normal_range_low),
    normal_range_high = VALUES(normal_range_high);

-- -----------------------------------------------------
-- measurement_types — LAB (common CBC, BMP, lipid, endocrine)
-- -----------------------------------------------------
INSERT INTO measurement_types (type_code, type_name, category, loinc_code, default_unit_id, normal_range_low, normal_range_high)
SELECT * FROM (
    -- CBC
    SELECT 'hemoglobin' AS type_code, 'Hemoglobin' AS type_name, 'lab' AS category, '718-7' AS loinc, 'g_dL' AS unit, 12.0  AS lo, 17.5   AS hi UNION ALL
    SELECT 'hematocrit',                'Hematocrit',              'lab', '4544-3',  'pct',   36.0,  50.0 UNION ALL
    SELECT 'wbc',                       'White Blood Cell Count',  'lab', '6690-2',  'K_uL',  4.5,   11.0 UNION ALL
    SELECT 'rbc',                       'Red Blood Cell Count',    'lab', '789-8',   'M_uL',  4.2,   5.9 UNION ALL
    SELECT 'platelets',                 'Platelet Count',          'lab', '777-3',   'K_uL',  150,   400 UNION ALL
    SELECT 'mcv',                       'Mean Corpuscular Volume', 'lab', '787-2',   'fL',    80,    100 UNION ALL
    -- BMP
    SELECT 'glucose',                   'Glucose (fasting)',       'lab', '1558-6',  'mg_dL', 70,    99 UNION ALL
    SELECT 'sodium',                    'Sodium',                  'lab', '2951-2',  'mmol_L',135,   145 UNION ALL
    SELECT 'potassium',                 'Potassium',               'lab', '2823-3',  'mmol_L',3.5,   5.0 UNION ALL
    SELECT 'chloride',                  'Chloride',                'lab', '2075-0',  'mmol_L',96,    106 UNION ALL
    SELECT 'co2',                       'Carbon Dioxide (Bicarb)', 'lab', '2028-9',  'mmol_L',23,    29 UNION ALL
    SELECT 'bun',                       'Blood Urea Nitrogen',     'lab', '3094-0',  'mg_dL', 7,     20 UNION ALL
    SELECT 'creatinine',                'Creatinine',              'lab', '2160-0',  'mg_dL', 0.6,   1.3 UNION ALL
    SELECT 'calcium',                   'Calcium',                 'lab', '17861-6', 'mg_dL', 8.5,   10.2 UNION ALL
    -- Lipid
    SELECT 'cholesterol_total',         'Cholesterol (Total)',     'lab', '2093-3',  'mg_dL', NULL,  200 UNION ALL
    SELECT 'ldl',                       'LDL Cholesterol',         'lab', '13457-7', 'mg_dL', NULL,  100 UNION ALL
    SELECT 'hdl',                       'HDL Cholesterol',         'lab', '2085-9',  'mg_dL', 40,    NULL UNION ALL
    SELECT 'triglycerides',             'Triglycerides',           'lab', '2571-8',  'mg_dL', NULL,  150 UNION ALL
    -- Endocrine
    SELECT 'tsh',                       'Thyroid Stimulating Hormone','lab','3016-3','U_L',   0.4,   4.0 UNION ALL
    SELECT 'hba1c',                     'Hemoglobin A1c',          'lab', '4548-4',  'pct',   4.0,   5.6
) AS v
JOIN measurement_units u ON u.unit_code = v.unit
ON DUPLICATE KEY UPDATE
    type_name         = VALUES(type_name),
    category          = VALUES(category),
    loinc_code        = VALUES(loinc_code),
    default_unit_id   = VALUES(default_unit_id),
    normal_range_low  = VALUES(normal_range_low),
    normal_range_high = VALUES(normal_range_high);

-- =====================================================
-- Verification (run manually)
-- =====================================================
-- SELECT category, COUNT(*) AS types FROM measurement_types GROUP BY category;
-- SELECT u.unit_code, COUNT(t.type_id) AS used_by_types
--   FROM measurement_units u
--   LEFT JOIN measurement_types t ON t.default_unit_id = u.unit_id
--   GROUP BY u.unit_code
--   ORDER BY used_by_types DESC;
