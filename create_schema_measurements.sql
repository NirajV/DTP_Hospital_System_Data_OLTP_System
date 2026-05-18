-- =====================================================
-- Hospital OLTP System — Clinical Measurements Migration
-- Implements Appendix C.6 of Requirement.md
-- =====================================================
-- Adds three tables to support unified (type, unit, value) capture
-- of vital signs and laboratory results:
--   * measurement_units    — UCUM-aligned unit lookup
--   * measurement_types    — measurement catalog (vital / lab / etc.)
--   * clinical_measurements — actual recorded values
--
-- Existing tables (encounter_vitals, lab_results) remain in place
-- for backward compatibility. New captures route through
-- clinical_measurements. See backfill_measurements.py.
-- =====================================================

USE hospital_OLTP_system;

-- -----------------------------------------------------
-- 1) Lookup: measurement_units
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS measurement_units (
    unit_id     INT AUTO_INCREMENT PRIMARY KEY,
    unit_code   VARCHAR(20)  NOT NULL UNIQUE COMMENT 'short identifier, e.g. mmHg',
    unit_name   VARCHAR(100) NOT NULL        COMMENT 'human-readable, e.g. Millimeters of Mercury',
    ucum_code   VARCHAR(20)                  COMMENT 'UCUM standard code where applicable',
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_unit_active (is_active)
);

-- -----------------------------------------------------
-- 2) Lookup: measurement_types
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS measurement_types (
    type_id           INT AUTO_INCREMENT PRIMARY KEY,
    type_code         VARCHAR(50)  NOT NULL UNIQUE COMMENT 'short identifier, e.g. bp_systolic',
    type_name         VARCHAR(150) NOT NULL        COMMENT 'human-readable, e.g. Blood Pressure (Systolic)',
    category          ENUM('vital_sign','lab','anthropometric','other') NOT NULL,
    loinc_code        VARCHAR(20)                  COMMENT 'LOINC for interoperability',
    default_unit_id   INT                          COMMENT 'preferred unit for this measurement',
    normal_range_low  DECIMAL(15,4)                COMMENT 'lower bound for abnormal flag',
    normal_range_high DECIMAL(15,4)                COMMENT 'upper bound for abnormal flag',
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type_category (category),
    INDEX idx_type_active (is_active)
);

-- -----------------------------------------------------
-- 3) Core: clinical_measurements
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS clinical_measurements (
    measurement_id  BIGINT AUTO_INCREMENT PRIMARY KEY,
    encounter_id    INT NOT NULL,
    patient_id      INT NOT NULL              COMMENT 'denormalized for fast patient-timeline queries',
    type_id         INT NOT NULL,
    unit_id         INT NOT NULL,
    value_numeric   DECIMAL(15,4)             COMMENT 'preferred for numeric measurements',
    value_text      VARCHAR(255)              COMMENT 'qualitative results, e.g. "positive"',
    recorded_by     INT NOT NULL              COMMENT 'FK -> users.user_id',
    recorded_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_abnormal     BOOLEAN DEFAULT FALSE     COMMENT 'computed against measurement_types.normal_range_*',
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_cm_value CHECK (value_numeric IS NOT NULL OR value_text IS NOT NULL),
    INDEX idx_cm_patient_recorded (patient_id, recorded_at DESC),
    INDEX idx_cm_encounter (encounter_id),
    INDEX idx_cm_type (type_id),
    INDEX idx_cm_recorded_by (recorded_by),
    INDEX idx_cm_abnormal (is_abnormal)
);

-- =====================================================
-- FOREIGN KEYS  (added separately to match existing project style)
-- =====================================================

ALTER TABLE measurement_types
    ADD CONSTRAINT fk_mtype_unit
    FOREIGN KEY (default_unit_id) REFERENCES measurement_units(unit_id)
    ON DELETE SET NULL;

ALTER TABLE clinical_measurements
    ADD CONSTRAINT fk_cm_encounter
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
    ON DELETE CASCADE;

ALTER TABLE clinical_measurements
    ADD CONSTRAINT fk_cm_patient
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
    ON DELETE CASCADE;

ALTER TABLE clinical_measurements
    ADD CONSTRAINT fk_cm_type
    FOREIGN KEY (type_id) REFERENCES measurement_types(type_id)
    ON DELETE RESTRICT;

ALTER TABLE clinical_measurements
    ADD CONSTRAINT fk_cm_unit
    FOREIGN KEY (unit_id) REFERENCES measurement_units(unit_id)
    ON DELETE RESTRICT;

ALTER TABLE clinical_measurements
    ADD CONSTRAINT fk_cm_recorder
    FOREIGN KEY (recorded_by) REFERENCES users(user_id)
    ON DELETE RESTRICT;

-- =====================================================
-- Verification queries (run manually after migration)
-- =====================================================
-- SHOW TABLES LIKE 'measurement%';
-- SHOW TABLES LIKE 'clinical_measurements';
-- SHOW CREATE TABLE clinical_measurements;
