-- Active: 1769437383812@@127.0.0.1@3306@hospital_oltp_system
-- Hospital OLTP System Database Schema
-- Database: hospital_OLTP_system
-- Comprehensive schema with ~50 tables covering all hospital operations

CREATE DATABASE IF NOT EXISTS hospital_OLTP_system;
USE hospital_OLTP_system;

-- =====================================================
-- DROP EXISTING TABLES (Simplified)
-- =====================================================
-- Disable FK checks to allow table drops without dependency issues
SET FOREIGN_KEY_CHECKS=0;

-- Drop all tables (FKs dropped automatically with tables)
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS payment_transactions;
DROP TABLE IF EXISTS invoice_items;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS insurance_claim_items;
DROP TABLE IF EXISTS insurance_claims;
DROP TABLE IF EXISTS insurance_authorizations;
DROP TABLE IF EXISTS patient_insurance_policies;
DROP TABLE IF EXISTS insurance_plans;
DROP TABLE IF EXISTS insurance_companies;
DROP TABLE IF EXISTS pharmacy_orders;
DROP TABLE IF EXISTS medication_inventory;
DROP TABLE IF EXISTS prescription_refills;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS drug_interactions;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS radiology_results;
DROP TABLE IF EXISTS radiology_orders;
DROP TABLE IF EXISTS lab_results;
DROP TABLE IF EXISTS lab_tests;
DROP TABLE IF EXISTS lab_orders;
DROP TABLE IF EXISTS encounter_procedures;
DROP TABLE IF EXISTS encounter_diagnoses;
DROP TABLE IF EXISTS encounter_vitals;
DROP TABLE IF EXISTS clinical_notes;
DROP TABLE IF EXISTS encounters;
DROP TABLE IF EXISTS appointment_cancellations;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS appointment_types;
DROP TABLE IF EXISTS doctor_schedules;
DROP TABLE IF EXISTS staff_shifts;
DROP TABLE IF EXISTS nurse_assignments;
DROP TABLE IF EXISTS nurses;
DROP TABLE IF EXISTS specialists;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS bed_assignments;
DROP TABLE IF EXISTS beds;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS facilities;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS department_equipment;
DROP TABLE IF EXISTS patient_allergies;
DROP TABLE IF EXISTS patient_emergency_contacts;
DROP TABLE IF EXISTS patient_addresses;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS icd_codes;
DROP TABLE IF EXISTS cpt_codes;

-- =====================================================
-- REFERENCE & LOOKUP TABLES
-- =====================================================

-- ICD Codes (International Classification of Diseases)
CREATE TABLE icd_codes (
    icd_id INT PRIMARY KEY AUTO_INCREMENT,
    icd_version VARCHAR(10) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_icd_code (code),
    INDEX idx_icd_category (category)
);

-- CPT Codes (Current Procedural Terminology)
CREATE TABLE cpt_codes (
    cpt_id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(10) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category VARCHAR(100),
    relative_value DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cpt_code (code),
    INDEX idx_cpt_category (category)
);

-- =====================================================
-- ORGANIZATIONAL STRUCTURE
-- =====================================================

-- Departments Table
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(20) UNIQUE,
    description TEXT,
    location VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    manager_id INT,
    budget DECIMAL(15,2),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_dept_status (status)
);

-- Facilities (Buildings, Wings, etc.)
CREATE TABLE facilities (
    facility_id INT PRIMARY KEY AUTO_INCREMENT,
    facility_name VARCHAR(100) NOT NULL,
    facility_type ENUM('building', 'wing', 'floor', 'unit') NOT NULL,
    address TEXT,
    total_capacity INT,
    status ENUM('active', 'maintenance', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Rooms
CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    facility_id INT NOT NULL,
    department_id INT,
    room_number VARCHAR(20) NOT NULL,
    room_type ENUM('patient', 'ICU', 'ER', 'operating', 'examination', 'consultation', 'laboratory', 'administrative') NOT NULL,
    floor_number INT,
    capacity INT DEFAULT 1,
    is_available BOOLEAN DEFAULT TRUE,
    status ENUM('available', 'occupied', 'maintenance', 'reserved') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_room_facility (facility_id),
    INDEX idx_room_type (room_type),
    INDEX idx_room_status (status)
);

-- Beds
CREATE TABLE beds (
    bed_id INT PRIMARY KEY AUTO_INCREMENT,
    room_id INT NOT NULL,
    bed_number VARCHAR(20) NOT NULL,
    bed_type ENUM('standard', 'ICU', 'pediatric', 'bariatric', 'isolation') NOT NULL,
    is_occupied BOOLEAN DEFAULT FALSE,
    status ENUM('available', 'occupied', 'maintenance', 'reserved') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_bed_room (room_id, bed_number),
    INDEX idx_bed_status (status),
    INDEX idx_bed_occupied (is_occupied)
);

-- Equipment
CREATE TABLE equipment (
    equipment_id INT PRIMARY KEY AUTO_INCREMENT,
    equipment_name VARCHAR(100) NOT NULL,
    equipment_type VARCHAR(50),
    manufacturer VARCHAR(100),
    model_number VARCHAR(100),
    serial_number VARCHAR(100) UNIQUE,
    purchase_date DATE,
    purchase_cost DECIMAL(12,2),
    warranty_expiry DATE,
    maintenance_schedule VARCHAR(50),
    last_maintenance DATE,
    next_maintenance DATE,
    status ENUM('available', 'in_use', 'maintenance', 'retired') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_equipment_type (equipment_type),
    INDEX idx_equipment_status (status)
);

-- Department Equipment Assignment
CREATE TABLE department_equipment (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    department_id INT NOT NULL,
    equipment_id INT NOT NULL,
    assigned_date DATE NOT NULL,
    return_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_dept_equip_dept (department_id),
    INDEX idx_dept_equip_equip (equipment_id)
);

-- =====================================================
-- PATIENT INFORMATION
-- =====================================================

-- Patients Table
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    mrn VARCHAR(50) UNIQUE NOT NULL COMMENT 'Medical Record Number',
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NOT NULL,
    ssn VARCHAR(20) UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(100),
    blood_group VARCHAR(5),
    marital_status ENUM('single', 'married', 'divorced', 'widowed', 'other'),
    occupation VARCHAR(100),
    preferred_language VARCHAR(50) DEFAULT 'English',
    registration_date DATE DEFAULT (CURRENT_DATE),
    photo_url VARCHAR(255),
    status ENUM('active', 'inactive', 'deceased') DEFAULT 'active',
    deceased_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_patient_name (last_name, first_name),
    INDEX idx_patient_mrn (mrn),
    INDEX idx_patient_dob (date_of_birth),
    INDEX idx_patient_status (status)
);

-- Patient Addresses
CREATE TABLE patient_addresses (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    address_type ENUM('home', 'work', 'billing', 'temporary') NOT NULL,
    street_address1 VARCHAR(255) NOT NULL,
    street_address2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) DEFAULT 'USA',
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_patient_addr (patient_id)
);

-- Patient Emergency Contacts
CREATE TABLE patient_emergency_contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50),
    phone VARCHAR(20) NOT NULL,
    alternate_phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    is_primary BOOLEAN DEFAULT FALSE,
    priority_order INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_emergency_patient (patient_id)
);

-- Patient Allergies
CREATE TABLE patient_allergies (
    allergy_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    allergen_name VARCHAR(100) NOT NULL,
    allergen_type ENUM('drug', 'food', 'environmental', 'other') NOT NULL,
    reaction TEXT,
    severity ENUM('mild', 'moderate', 'severe', 'life-threatening') NOT NULL,
    onset_date DATE,
    notes TEXT,
    status ENUM('active', 'inactive', 'resolved') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_allergy_patient (patient_id),
    INDEX idx_allergy_type (allergen_type),
    INDEX idx_allergy_status (status)
);

-- =====================================================
-- STAFF & HEALTHCARE PROVIDERS
-- =====================================================

-- Staff (Non-medical personnel)
CREATE TABLE staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department_id INT,
    position VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE,
    salary DECIMAL(12,2),
    status ENUM('active', 'on_leave', 'terminated') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_staff_dept (department_id),
    INDEX idx_staff_status (status)
);

-- Doctors Table (Enhanced)
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    sub_specialization VARCHAR(100),
    department_id INT,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_state VARCHAR(50),
    license_expiry DATE,
    board_certification VARCHAR(255),
    medical_school VARCHAR(255),
    graduation_year YEAR,
    npi_number VARCHAR(20) UNIQUE COMMENT 'National Provider Identifier',
    hire_date DATE NOT NULL,
    consultation_fee DECIMAL(10,2),
    status ENUM('active', 'on_leave', 'inactive', 'retired') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_doctor_dept (department_id),
    INDEX idx_doctor_specialization (specialization),
    INDEX idx_doctor_status (status),
    INDEX idx_doctor_npi (npi_number)
);

-- Specialists (Consulting doctors)
CREATE TABLE specialists (
    specialist_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    specialty_area VARCHAR(100) NOT NULL,
    certification_details TEXT,
    years_of_experience INT,
    available_for_consultation BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_specialist_doctor (doctor_id),
    INDEX idx_specialist_area (specialty_area)
);

-- Nurses
CREATE TABLE nurses (
    nurse_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department_id INT,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_type ENUM('RN', 'LPN', 'NP', 'CNS') NOT NULL COMMENT 'RN=Registered Nurse, LPN=Licensed Practical Nurse, NP=Nurse Practitioner, CNS=Clinical Nurse Specialist',
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    hire_date DATE NOT NULL,
    shift_preference ENUM('day', 'night', 'rotating') DEFAULT 'day',
    status ENUM('active', 'on_leave', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nurse_dept (department_id),
    INDEX idx_nurse_status (status)
);

-- Nurse Assignments
CREATE TABLE nurse_assignments (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    nurse_id INT NOT NULL,
    patient_id INT NOT NULL,
    bed_id INT,
    assigned_date DATETIME NOT NULL,
    end_date DATETIME,
    shift ENUM('day', 'evening', 'night') NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nurse_assign_nurse (nurse_id),
    INDEX idx_nurse_assign_patient (patient_id),
    INDEX idx_nurse_assign_date (assigned_date)
);

-- Staff Shifts
CREATE TABLE staff_shifts (
    shift_id INT PRIMARY KEY AUTO_INCREMENT,
    staff_id INT,
    nurse_id INT,
    shift_date DATE NOT NULL,
    shift_type ENUM('morning', 'afternoon', 'evening', 'night', 'overnight') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status ENUM('scheduled', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_shift_staff (staff_id),
    INDEX idx_shift_nurse (nurse_id),
    INDEX idx_shift_date (shift_date),
    CHECK ((staff_id IS NOT NULL) OR (nurse_id IS NOT NULL))
);

-- Doctor Schedules
CREATE TABLE doctor_schedules (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_id INT,
    max_patients INT DEFAULT 20,
    is_active BOOLEAN DEFAULT TRUE,
    effective_from DATE,
    effective_to DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_schedule_doctor (doctor_id),
    INDEX idx_schedule_day (day_of_week)
);

-- =====================================================
-- APPOINTMENTS & SCHEDULING
-- =====================================================

-- Appointment Types
CREATE TABLE appointment_types (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    default_duration INT DEFAULT 30 COMMENT 'Duration in minutes',
    color_code VARCHAR(7) COMMENT 'Hex color for calendar',
    requires_preparation BOOLEAN DEFAULT FALSE,
    preparation_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments Table (Enhanced)
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_number VARCHAR(50) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_type_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration_minutes INT DEFAULT 30,
    room_id INT,
    reason VARCHAR(255),
    chief_complaint TEXT,
    status ENUM('scheduled', 'confirmed', 'checked_in', 'in_progress', 'completed', 'cancelled', 'no_show', 'rescheduled') DEFAULT 'scheduled',
    priority ENUM('routine', 'urgent', 'emergency') DEFAULT 'routine',
    is_follow_up BOOLEAN DEFAULT FALSE,
    parent_appointment_id INT COMMENT 'Links to original appointment if follow-up',
    confirmation_sent BOOLEAN DEFAULT FALSE,
    reminder_sent BOOLEAN DEFAULT FALSE,
    notes TEXT,
    cancellation_reason TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_appointment_date (appointment_date),
    INDEX idx_appointment_patient (patient_id),
    INDEX idx_appointment_doctor (doctor_id),
    INDEX idx_appointment_status (status),
    INDEX idx_appointment_type (appointment_type_id)
);

-- Appointment Cancellations (Audit trail)
CREATE TABLE appointment_cancellations (
    cancellation_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT NOT NULL,
    cancelled_by ENUM('patient', 'doctor', 'staff', 'system') NOT NULL,
    cancellation_date DATETIME NOT NULL,
    reason TEXT NOT NULL,
    reschedule_requested BOOLEAN DEFAULT FALSE,
    new_appointment_id INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cancel_appointment (appointment_id)
);

-- =====================================================
-- ENCOUNTERS & VISITS
-- =====================================================

-- Encounters (Patient Visits)
CREATE TABLE encounters (
    encounter_id INT PRIMARY KEY AUTO_INCREMENT,
    encounter_number VARCHAR(50) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_id INT,
    encounter_date DATETIME NOT NULL,
    encounter_type ENUM('outpatient', 'inpatient', 'emergency', 'surgical', 'consultation') NOT NULL,
    department_id INT,
    room_id INT,
    bed_id INT,
    chief_complaint TEXT,
    present_illness TEXT,
    admission_date DATETIME,
    discharge_date DATETIME,
    length_of_stay INT COMMENT 'Days',
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
    discharge_disposition ENUM('home', 'transferred', 'admitted', 'expired', 'left_ama') COMMENT 'AMA = Against Medical Advice',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_encounter_patient (patient_id),
    INDEX idx_encounter_doctor (doctor_id),
    INDEX idx_encounter_date (encounter_date),
    INDEX idx_encounter_type (encounter_type),
    INDEX idx_encounter_status (status)
);

-- Encounter Vitals
CREATE TABLE encounter_vitals (
    vital_id INT PRIMARY KEY AUTO_INCREMENT,
    encounter_id INT NOT NULL,
    recorded_datetime DATETIME NOT NULL,
    recorded_by INT COMMENT 'Staff or Nurse ID',
    temperature DECIMAL(4,1) COMMENT 'Fahrenheit',
    blood_pressure_systolic INT,
    blood_pressure_diastolic INT,
    heart_rate INT COMMENT 'Beats per minute',
    respiratory_rate INT COMMENT 'Breaths per minute',
    oxygen_saturation DECIMAL(5,2) COMMENT 'Percentage',
    weight DECIMAL(5,2) COMMENT 'Pounds',
    height DECIMAL(5,2) COMMENT 'Inches',
    bmi DECIMAL(4,2) COMMENT 'Body Mass Index',
    pain_score INT COMMENT '0-10 scale',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vitals_encounter (encounter_id),
    INDEX idx_vitals_datetime (recorded_datetime)
);

-- Encounter Diagnoses
CREATE TABLE encounter_diagnoses (
    diagnosis_id INT PRIMARY KEY AUTO_INCREMENT,
    encounter_id INT NOT NULL,
    icd_code_id INT NOT NULL,
    diagnosis_type ENUM('primary', 'secondary', 'differential', 'rule_out') DEFAULT 'primary',
    diagnosis_description TEXT NOT NULL,
    severity ENUM('mild', 'moderate', 'severe', 'critical'),
    onset_date DATE,
    resolution_date DATE,
    is_chronic BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_diag_encounter (encounter_id),
    INDEX idx_diag_icd (icd_code_id)
);

-- Encounter Procedures
CREATE TABLE encounter_procedures (
    procedure_id INT PRIMARY KEY AUTO_INCREMENT,
    encounter_id INT NOT NULL,
    cpt_code_id INT NOT NULL,
    procedure_name VARCHAR(255) NOT NULL,
    procedure_description TEXT,
    performed_by INT COMMENT 'Doctor ID',
    assisted_by TEXT COMMENT 'Comma-separated IDs',
    procedure_datetime DATETIME NOT NULL,
    duration_minutes INT,
    room_id INT,
    anesthesia_type ENUM('none', 'local', 'regional', 'general', 'sedation'),
    outcome TEXT,
    complications TEXT,
    notes TEXT,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_proc_encounter (encounter_id),
    INDEX idx_proc_cpt (cpt_code_id),
    INDEX idx_proc_datetime (procedure_datetime)
);

-- Clinical Notes
CREATE TABLE clinical_notes (
    note_id INT PRIMARY KEY AUTO_INCREMENT,
    encounter_id INT NOT NULL,
    note_type ENUM('progress', 'admission', 'discharge', 'operative', 'consultation', 'nursing') NOT NULL,
    author_id INT NOT NULL COMMENT 'Doctor/Nurse/Staff ID',
    author_type ENUM('doctor', 'nurse', 'staff') NOT NULL,
    note_datetime DATETIME NOT NULL,
    subject VARCHAR(255),
    note_text TEXT NOT NULL,
    is_signed BOOLEAN DEFAULT FALSE,
    signed_datetime DATETIME,
    is_amended BOOLEAN DEFAULT FALSE,
    amendment_note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_notes_encounter (encounter_id),
    INDEX idx_notes_type (note_type),
    INDEX idx_notes_datetime (note_datetime)
);

-- Bed Assignments
CREATE TABLE bed_assignments (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    bed_id INT NOT NULL,
    encounter_id INT,
    assignment_datetime DATETIME NOT NULL,
    discharge_datetime DATETIME,
    reason TEXT,
    assigned_by INT COMMENT 'Staff ID',
    status ENUM('active', 'discharged', 'transferred') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bed_assign_patient (patient_id),
    INDEX idx_bed_assign_bed (bed_id),
    INDEX idx_bed_assign_status (status)
);

-- =====================================================
-- LABORATORY & DIAGNOSTICS
-- =====================================================

-- Lab Orders
CREATE TABLE lab_orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    encounter_id INT NOT NULL,
    patient_id INT NOT NULL,
    ordering_doctor_id INT NOT NULL,
    order_datetime DATETIME NOT NULL,
    priority ENUM('routine', 'urgent', 'stat') DEFAULT 'routine',
    status ENUM('ordered', 'collected', 'in_progress', 'completed', 'cancelled') DEFAULT 'ordered',
    collection_datetime DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_lab_order_encounter (encounter_id),
    INDEX idx_lab_order_patient (patient_id),
    INDEX idx_lab_order_status (status)
);

-- Lab Tests
CREATE TABLE lab_tests (
    test_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    test_code VARCHAR(20) NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    test_category VARCHAR(100),
    specimen_type VARCHAR(100),
    status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_test_order (order_id),
    INDEX idx_test_code (test_code)
);

-- Lab Results
CREATE TABLE lab_results (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    test_id INT NOT NULL,
    result_value VARCHAR(255),
    result_unit VARCHAR(50),
    reference_range VARCHAR(100),
    abnormal_flag ENUM('normal', 'low', 'high', 'critical') DEFAULT 'normal',
    result_datetime DATETIME NOT NULL,
    performed_by VARCHAR(100),
    verified_by INT COMMENT 'Doctor ID',
    verification_datetime DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_result_test (test_id),
    INDEX idx_result_datetime (result_datetime)
);

-- Radiology Orders
CREATE TABLE radiology_orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    encounter_id INT NOT NULL,
    patient_id INT NOT NULL,
    ordering_doctor_id INT NOT NULL,
    exam_type VARCHAR(100) NOT NULL,
    body_part VARCHAR(100) NOT NULL,
    modality ENUM('X-Ray', 'CT', 'MRI', 'Ultrasound', 'PET', 'Mammography', 'Fluoroscopy') NOT NULL,
    order_datetime DATETIME NOT NULL,
    scheduled_datetime DATETIME,
    priority ENUM('routine', 'urgent', 'stat') DEFAULT 'routine',
    clinical_indication TEXT,
    contrast_used BOOLEAN DEFAULT FALSE,
    status ENUM('ordered', 'scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'ordered',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rad_order_encounter (encounter_id),
    INDEX idx_rad_order_patient (patient_id),
    INDEX idx_rad_order_status (status)
);

-- Radiology Results
CREATE TABLE radiology_results (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    exam_datetime DATETIME NOT NULL,
    radiologist_id INT NOT NULL,
    findings TEXT NOT NULL,
    impression TEXT NOT NULL,
    report_text TEXT,
    critical_findings BOOLEAN DEFAULT FALSE,
    report_datetime DATETIME NOT NULL,
    image_location VARCHAR(255) COMMENT 'PACS system reference',
    status ENUM('preliminary', 'final', 'amended') DEFAULT 'preliminary',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rad_result_order (order_id),
    INDEX idx_rad_result_datetime (exam_datetime)
);

-- =====================================================
-- PHARMACY & MEDICATIONS
-- =====================================================

-- Medications
CREATE TABLE medications (
    medication_id INT PRIMARY KEY AUTO_INCREMENT,
    medication_name VARCHAR(200) NOT NULL,
    generic_name VARCHAR(200),
    brand_name VARCHAR(200),
    drug_class VARCHAR(100),
    ndc_code VARCHAR(20) UNIQUE COMMENT 'National Drug Code',
    dosage_form ENUM('tablet', 'capsule', 'liquid', 'injection', 'cream', 'inhaler', 'patch', 'drops') NOT NULL,
    strength VARCHAR(50),
    unit_of_measure VARCHAR(20),
    manufacturer VARCHAR(200),
    is_controlled BOOLEAN DEFAULT FALSE,
    dea_schedule VARCHAR(5) COMMENT 'DEA Schedule (I-V)',
    requires_prescription BOOLEAN DEFAULT TRUE,
    unit_price DECIMAL(10,2),
    status ENUM('active', 'discontinued', 'recalled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_med_name (medication_name),
    INDEX idx_med_generic (generic_name),
    INDEX idx_med_ndc (ndc_code),
    INDEX idx_med_class (drug_class)
);

-- Drug Interactions
CREATE TABLE drug_interactions (
    interaction_id INT PRIMARY KEY AUTO_INCREMENT,
    medication_id_1 INT NOT NULL,
    medication_id_2 INT NOT NULL,
    interaction_type ENUM('major', 'moderate', 'minor') NOT NULL,
    description TEXT NOT NULL,
    clinical_effect TEXT,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_interaction (medication_id_1, medication_id_2),
    INDEX idx_interaction_med1 (medication_id_1),
    INDEX idx_interaction_med2 (medication_id_2)
);

-- Prescriptions Table (Enhanced)
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    prescription_number VARCHAR(50) UNIQUE NOT NULL,
    encounter_id INT NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    medication_id INT NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    dosage_unit VARCHAR(20),
    route ENUM('oral', 'IV', 'IM', 'subcutaneous', 'topical', 'inhalation', 'rectal', 'sublingual') NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100),
    quantity_prescribed INT NOT NULL,
    quantity_dispensed INT,
    refills_allowed INT DEFAULT 0,
    refills_remaining INT,
    prescription_date DATE NOT NULL,
    start_date DATE,
    end_date DATE,
    instructions TEXT,
    indication TEXT,
    pharmacy_notes TEXT,
    prescriber_signature VARCHAR(255),
    status ENUM('active', 'completed', 'discontinued', 'cancelled', 'expired') DEFAULT 'active',
    discontinuation_reason TEXT,
    is_refill BOOLEAN DEFAULT FALSE,
    original_prescription_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rx_encounter (encounter_id),
    INDEX idx_rx_patient (patient_id),
    INDEX idx_rx_doctor (doctor_id),
    INDEX idx_rx_medication (medication_id),
    INDEX idx_rx_date (prescription_date),
    INDEX idx_rx_status (status)
);

-- Prescription Refills
CREATE TABLE prescription_refills (
    refill_id INT PRIMARY KEY AUTO_INCREMENT,
    prescription_id INT NOT NULL,
    refill_number INT NOT NULL,
    refill_date DATE NOT NULL,
    quantity_dispensed INT NOT NULL,
    dispensed_by VARCHAR(100),
    pharmacy_name VARCHAR(200),
    pharmacy_phone VARCHAR(20),
    cost DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_refill_prescription (prescription_id),
    INDEX idx_refill_date (refill_date)
);

-- Medication Inventory
CREATE TABLE medication_inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    medication_id INT NOT NULL,
    lot_number VARCHAR(50),
    expiration_date DATE NOT NULL,
    quantity_on_hand INT NOT NULL DEFAULT 0,
    reorder_level INT DEFAULT 100,
    location VARCHAR(100),
    last_restock_date DATE,
    last_restock_quantity INT,
    status ENUM('available', 'low_stock', 'expired', 'recalled') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_inventory_med (medication_id),
    INDEX idx_inventory_status (status),
    INDEX idx_inventory_expiry (expiration_date)
);

-- Pharmacy Orders (for inventory management)
CREATE TABLE pharmacy_orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    medication_id INT NOT NULL,
    supplier_name VARCHAR(200) NOT NULL,
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    quantity_ordered INT NOT NULL,
    quantity_received INT,
    unit_cost DECIMAL(10,2),
    total_cost DECIMAL(12,2),
    order_status ENUM('pending', 'approved', 'ordered', 'partially_received', 'received', 'cancelled') DEFAULT 'pending',
    ordered_by INT COMMENT 'Staff ID',
    received_by INT COMMENT 'Staff ID',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_pharm_order_med (medication_id),
    INDEX idx_pharm_order_status (order_status),
    INDEX idx_pharm_order_date (order_date)
);

-- =====================================================
-- INSURANCE & BILLING
-- =====================================================

-- Insurance Companies
CREATE TABLE insurance_companies (
    insurance_company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(200) NOT NULL UNIQUE,
    company_code VARCHAR(20) UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    address TEXT,
    contact_person VARCHAR(100),
    contact_phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_insurance_name (company_name),
    INDEX idx_insurance_active (is_active)
);

-- Insurance Plans
CREATE TABLE insurance_plans (
    plan_id INT PRIMARY KEY AUTO_INCREMENT,
    insurance_company_id INT NOT NULL,
    plan_name VARCHAR(200) NOT NULL,
    plan_code VARCHAR(50),
    plan_type ENUM('HMO', 'PPO', 'EPO', 'POS', 'Medicare', 'Medicaid', 'Other') NOT NULL,
    coverage_level ENUM('individual', 'family', 'employee_spouse', 'employee_children') NOT NULL,
    deductible_amount DECIMAL(10,2),
    copay_amount DECIMAL(10,2),
    out_of_pocket_max DECIMAL(10,2),
    coverage_percentage DECIMAL(5,2),
    effective_date DATE,
    termination_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_plan_company (insurance_company_id),
    INDEX idx_plan_type (plan_type),
    INDEX idx_plan_active (is_active)
);

-- Patient Insurance Policies
CREATE TABLE patient_insurance_policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    insurance_plan_id INT NOT NULL,
    policy_number VARCHAR(100) NOT NULL,
    group_number VARCHAR(100),
    subscriber_name VARCHAR(100),
    subscriber_relationship ENUM('self', 'spouse', 'child', 'parent', 'other') NOT NULL,
    subscriber_dob DATE,
    subscriber_ssn VARCHAR(20),
    policy_start_date DATE NOT NULL,
    policy_end_date DATE,
    is_primary BOOLEAN DEFAULT TRUE,
    priority_order INT DEFAULT 1,
    status ENUM('active', 'inactive', 'expired', 'cancelled') DEFAULT 'active',
    verification_date DATE,
    verified_by INT COMMENT 'Staff ID',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_policy_patient (patient_id),
    INDEX idx_policy_plan (insurance_plan_id),
    INDEX idx_policy_status (status)
);

-- Insurance Authorizations
CREATE TABLE insurance_authorizations (
    authorization_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    policy_id INT NOT NULL,
    authorization_number VARCHAR(100) UNIQUE NOT NULL,
    service_type VARCHAR(200) NOT NULL,
    cpt_code_id INT,
    units_authorized INT,
    units_used INT DEFAULT 0,
    authorization_date DATE NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    status ENUM('pending', 'approved', 'denied', 'expired', 'cancelled') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_auth_patient (patient_id),
    INDEX idx_auth_policy (policy_id),
    INDEX idx_auth_status (status)
);

-- Insurance Claims
CREATE TABLE insurance_claims (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    claim_number VARCHAR(100) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    policy_id INT NOT NULL,
    encounter_id INT NOT NULL,
    claim_date DATE NOT NULL,
    service_date_from DATE NOT NULL,
    service_date_to DATE,
    total_charge DECIMAL(12,2) NOT NULL,
    allowed_amount DECIMAL(12,2),
    paid_amount DECIMAL(12,2) DEFAULT 0,
    patient_responsibility DECIMAL(12,2),
    adjustment_amount DECIMAL(12,2) DEFAULT 0,
    submission_date DATE,
    adjudication_date DATE,
    payment_date DATE,
    status ENUM('draft', 'submitted', 'pending', 'approved', 'partially_paid', 'paid', 'denied', 'appealed') DEFAULT 'draft',
    denial_reason TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_claim_patient (patient_id),
    INDEX idx_claim_policy (policy_id),
    INDEX idx_claim_encounter (encounter_id),
    INDEX idx_claim_status (status),
    INDEX idx_claim_date (claim_date)
);

-- Insurance Claim Items
CREATE TABLE insurance_claim_items (
    claim_item_id INT PRIMARY KEY AUTO_INCREMENT,
    claim_id INT NOT NULL,
    line_number INT NOT NULL,
    service_date DATE NOT NULL,
    cpt_code_id INT,
    icd_code_id INT,
    service_description TEXT,
    quantity INT DEFAULT 1,
    unit_charge DECIMAL(10,2) NOT NULL,
    total_charge DECIMAL(12,2) NOT NULL,
    allowed_amount DECIMAL(12,2),
    paid_amount DECIMAL(12,2) DEFAULT 0,
    adjustment_amount DECIMAL(12,2) DEFAULT 0,
    adjustment_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_claim_item_claim (claim_id),
    INDEX idx_claim_item_cpt (cpt_code_id),
    INDEX idx_claim_item_icd (icd_code_id)
);

-- Invoices (Patient Billing)
CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    encounter_id INT,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    subtotal_amount DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    amount_paid DECIMAL(12,2) DEFAULT 0,
    amount_due DECIMAL(12,2) GENERATED ALWAYS AS (total_amount - amount_paid) STORED,
    insurance_paid DECIMAL(12,2) DEFAULT 0,
    patient_responsibility DECIMAL(12,2),
    payment_status ENUM('pending', 'partial', 'paid', 'overdue', 'cancelled') DEFAULT 'pending',
    payment_terms VARCHAR(100),
    notes TEXT,
    created_by INT COMMENT 'Staff ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_invoice_patient (patient_id),
    INDEX idx_invoice_encounter (encounter_id),
    INDEX idx_invoice_status (payment_status),
    INDEX idx_invoice_date (invoice_date)
);

-- Invoice Items
CREATE TABLE invoice_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    invoice_id INT NOT NULL,
    line_number INT NOT NULL,
    item_type ENUM('service', 'procedure', 'medication', 'lab', 'radiology', 'supply', 'room_charge', 'other') NOT NULL,
    cpt_code_id INT,
    description TEXT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_item_invoice (invoice_id),
    INDEX idx_item_type (item_type)
);

-- Payment Transactions
CREATE TABLE payment_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_number VARCHAR(100) UNIQUE NOT NULL,
    invoice_id INT NOT NULL,
    patient_id INT NOT NULL,
    payment_date DATE NOT NULL,
    payment_amount DECIMAL(12,2) NOT NULL,
    payment_method ENUM('cash', 'check', 'credit_card', 'debit_card', 'insurance', 'bank_transfer', 'online', 'other') NOT NULL,
    payment_reference VARCHAR(100) COMMENT 'Check number, transaction ID, etc.',
    card_type VARCHAR(50),
    card_last_four VARCHAR(4),
    processed_by INT COMMENT 'Staff ID',
    notes TEXT,
    status ENUM('pending', 'completed', 'failed', 'refunded', 'cancelled') DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_payment_invoice (invoice_id),
    INDEX idx_payment_patient (patient_id),
    INDEX idx_payment_date (payment_date),
    INDEX idx_payment_status (status)
);

-- =====================================================
-- SYSTEM & ADMINISTRATIVE
-- =====================================================

-- Users (System Access)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type ENUM('doctor', 'nurse', 'staff', 'admin', 'receptionist') NOT NULL,
    reference_id INT COMMENT 'Links to doctor_id, nurse_id, or staff_id',
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME,
    password_changed_at TIMESTAMP,
    failed_login_attempts INT DEFAULT 0,
    account_locked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_username (username),
    INDEX idx_user_email (email),
    INDEX idx_user_type (user_type)
);

-- Roles
CREATE TABLE roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions TEXT COMMENT 'JSON format permissions',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User Roles Assignment
CREATE TABLE user_roles (
    user_role_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_date DATE NOT NULL,
    assigned_by INT COMMENT 'Admin user ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_role (user_id, role_id)
);

-- Audit Logs
CREATE TABLE audit_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100) NOT NULL,
    record_id INT NOT NULL,
    action ENUM('INSERT', 'UPDATE', 'DELETE', 'VIEW') NOT NULL,
    user_id INT,
    user_type VARCHAR(50),
    old_values TEXT COMMENT 'JSON format',
    new_values TEXT COMMENT 'JSON format',
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_table (table_name),
    INDEX idx_audit_record (record_id),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_timestamp (timestamp)
);
-- CREATE TABLE departments (
--     department_id INT PRIMARY KEY AUTO_INCREMENT,
--     department_name VARCHAR(100) NOT NULL UNIQUE,
--     location VARCHAR(100),
--     phone VARCHAR(20),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- =====================================================
-- BUILD FOREIGN KEY RELATIONSHIPS
-- =====================================================

-- Foreign Keys for rooms table
ALTER TABLE rooms ADD CONSTRAINT fk_rooms_facility FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE;
ALTER TABLE rooms ADD CONSTRAINT fk_rooms_department FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL;

-- Foreign Keys for beds table
ALTER TABLE beds ADD CONSTRAINT fk_beds_room FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE;

-- Foreign Keys for department_equipment table
ALTER TABLE department_equipment ADD CONSTRAINT fk_dept_equip_dept FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE;
ALTER TABLE department_equipment ADD CONSTRAINT fk_dept_equip_equip FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE;

-- Foreign Keys for patient_addresses table
ALTER TABLE patient_addresses ADD CONSTRAINT fk_patient_addr FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;

-- Foreign Keys for patient_emergency_contacts table
ALTER TABLE patient_emergency_contacts ADD CONSTRAINT fk_emergency_contact FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;

-- Foreign Keys for patient_allergies table
ALTER TABLE patient_allergies ADD CONSTRAINT fk_allergy_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;

-- Foreign Keys for staff table
ALTER TABLE staff ADD CONSTRAINT fk_staff_dept FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL;

-- Foreign Keys for doctors table
ALTER TABLE doctors ADD CONSTRAINT fk_doctors_dept FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL;

-- Foreign Keys for specialists table
ALTER TABLE specialists ADD CONSTRAINT fk_specialist_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;

-- Foreign Keys for nurses table
ALTER TABLE nurses ADD CONSTRAINT fk_nurses_dept FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL;

-- Foreign Keys for nurse_assignments table
ALTER TABLE nurse_assignments ADD CONSTRAINT fk_nurse_assign_nurse FOREIGN KEY (nurse_id) REFERENCES nurses(nurse_id) ON DELETE CASCADE;
ALTER TABLE nurse_assignments ADD CONSTRAINT fk_nurse_assign_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE nurse_assignments ADD CONSTRAINT fk_nurse_assign_bed FOREIGN KEY (bed_id) REFERENCES beds(bed_id) ON DELETE SET NULL;

-- Foreign Keys for staff_shifts table
ALTER TABLE staff_shifts ADD CONSTRAINT fk_shift_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE;
ALTER TABLE staff_shifts ADD CONSTRAINT fk_shift_nurse FOREIGN KEY (nurse_id) REFERENCES nurses(nurse_id) ON DELETE CASCADE;

-- Foreign Keys for doctor_schedules table
ALTER TABLE doctor_schedules ADD CONSTRAINT fk_schedule_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;
ALTER TABLE doctor_schedules ADD CONSTRAINT fk_schedule_room FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL;

-- Foreign Keys for appointments table
ALTER TABLE appointments ADD CONSTRAINT fk_appt_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE appointments ADD CONSTRAINT fk_appt_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;
ALTER TABLE appointments ADD CONSTRAINT fk_appt_type FOREIGN KEY (appointment_type_id) REFERENCES appointment_types(type_id) ON DELETE SET NULL;
ALTER TABLE appointments ADD CONSTRAINT fk_appt_room FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL;
ALTER TABLE appointments ADD CONSTRAINT fk_appt_parent FOREIGN KEY (parent_appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL;

-- Foreign Keys for appointment_cancellations table
ALTER TABLE appointment_cancellations ADD CONSTRAINT fk_cancel_appt FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE;
ALTER TABLE appointment_cancellations ADD CONSTRAINT fk_cancel_new_appt FOREIGN KEY (new_appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL;

-- Foreign Keys for encounters table
ALTER TABLE encounters ADD CONSTRAINT fk_encounter_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE encounters ADD CONSTRAINT fk_encounter_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;
ALTER TABLE encounters ADD CONSTRAINT fk_encounter_appt FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL;
ALTER TABLE encounters ADD CONSTRAINT fk_encounter_dept FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL;
ALTER TABLE encounters ADD CONSTRAINT fk_encounter_room FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL;
ALTER TABLE encounters ADD CONSTRAINT fk_encounter_bed FOREIGN KEY (bed_id) REFERENCES beds(bed_id) ON DELETE SET NULL;

-- Foreign Keys for encounter_vitals table
ALTER TABLE encounter_vitals ADD CONSTRAINT fk_vitals_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;

-- Foreign Keys for encounter_diagnoses table
ALTER TABLE encounter_diagnoses ADD CONSTRAINT fk_diag_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;
ALTER TABLE encounter_diagnoses ADD CONSTRAINT fk_diag_icd FOREIGN KEY (icd_code_id) REFERENCES icd_codes(icd_id) ON DELETE RESTRICT;

-- Foreign Keys for encounter_procedures table
ALTER TABLE encounter_procedures ADD CONSTRAINT fk_proc_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;
ALTER TABLE encounter_procedures ADD CONSTRAINT fk_proc_cpt FOREIGN KEY (cpt_code_id) REFERENCES cpt_codes(cpt_id) ON DELETE RESTRICT;
ALTER TABLE encounter_procedures ADD CONSTRAINT fk_proc_room FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL;

-- Foreign Keys for clinical_notes table
ALTER TABLE clinical_notes ADD CONSTRAINT fk_notes_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;

-- Foreign Keys for bed_assignments table
ALTER TABLE bed_assignments ADD CONSTRAINT fk_bed_assign_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE bed_assignments ADD CONSTRAINT fk_bed_assign_bed FOREIGN KEY (bed_id) REFERENCES beds(bed_id) ON DELETE CASCADE;
ALTER TABLE bed_assignments ADD CONSTRAINT fk_bed_assign_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE SET NULL;

-- Foreign Keys for lab_orders table
ALTER TABLE lab_orders ADD CONSTRAINT fk_lab_order_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;
ALTER TABLE lab_orders ADD CONSTRAINT fk_lab_order_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE lab_orders ADD CONSTRAINT fk_lab_order_doctor FOREIGN KEY (ordering_doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;

-- Foreign Keys for lab_tests table
ALTER TABLE lab_tests ADD CONSTRAINT fk_test_order FOREIGN KEY (order_id) REFERENCES lab_orders(order_id) ON DELETE CASCADE;

-- Foreign Keys for lab_results table
ALTER TABLE lab_results ADD CONSTRAINT fk_result_test FOREIGN KEY (test_id) REFERENCES lab_tests(test_id) ON DELETE CASCADE;

-- Foreign Keys for radiology_orders table
ALTER TABLE radiology_orders ADD CONSTRAINT fk_rad_order_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;
ALTER TABLE radiology_orders ADD CONSTRAINT fk_rad_order_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE radiology_orders ADD CONSTRAINT fk_rad_order_doctor FOREIGN KEY (ordering_doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;

-- Foreign Keys for radiology_results table
ALTER TABLE radiology_results ADD CONSTRAINT fk_rad_result_order FOREIGN KEY (order_id) REFERENCES radiology_orders(order_id) ON DELETE CASCADE;
ALTER TABLE radiology_results ADD CONSTRAINT fk_rad_result_radiologist FOREIGN KEY (radiologist_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;

-- Foreign Keys for drug_interactions table
ALTER TABLE drug_interactions ADD CONSTRAINT fk_interaction_med1 FOREIGN KEY (medication_id_1) REFERENCES medications(medication_id) ON DELETE CASCADE;
ALTER TABLE drug_interactions ADD CONSTRAINT fk_interaction_med2 FOREIGN KEY (medication_id_2) REFERENCES medications(medication_id) ON DELETE CASCADE;

-- Foreign Keys for prescriptions table
ALTER TABLE prescriptions ADD CONSTRAINT fk_rx_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;
ALTER TABLE prescriptions ADD CONSTRAINT fk_rx_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE prescriptions ADD CONSTRAINT fk_rx_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE;
ALTER TABLE prescriptions ADD CONSTRAINT fk_rx_medication FOREIGN KEY (medication_id) REFERENCES medications(medication_id) ON DELETE RESTRICT;
ALTER TABLE prescriptions ADD CONSTRAINT fk_rx_original FOREIGN KEY (original_prescription_id) REFERENCES prescriptions(prescription_id) ON DELETE SET NULL;

-- Foreign Keys for prescription_refills table
ALTER TABLE prescription_refills ADD CONSTRAINT fk_refill_rx FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON DELETE CASCADE;

-- Foreign Keys for medication_inventory table
ALTER TABLE medication_inventory ADD CONSTRAINT fk_inventory_med FOREIGN KEY (medication_id) REFERENCES medications(medication_id) ON DELETE CASCADE;

-- Foreign Keys for pharmacy_orders table
ALTER TABLE pharmacy_orders ADD CONSTRAINT fk_pharm_order_med FOREIGN KEY (medication_id) REFERENCES medications(medication_id) ON DELETE RESTRICT;

-- Foreign Keys for insurance_plans table
ALTER TABLE insurance_plans ADD CONSTRAINT fk_plan_company FOREIGN KEY (insurance_company_id) REFERENCES insurance_companies(insurance_company_id) ON DELETE CASCADE;

-- Foreign Keys for patient_insurance_policies table
ALTER TABLE patient_insurance_policies ADD CONSTRAINT fk_policy_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE patient_insurance_policies ADD CONSTRAINT fk_policy_plan FOREIGN KEY (insurance_plan_id) REFERENCES insurance_plans(plan_id) ON DELETE RESTRICT;

-- Foreign Keys for insurance_authorizations table
ALTER TABLE insurance_authorizations ADD CONSTRAINT fk_auth_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE insurance_authorizations ADD CONSTRAINT fk_auth_policy FOREIGN KEY (policy_id) REFERENCES patient_insurance_policies(policy_id) ON DELETE CASCADE;
ALTER TABLE insurance_authorizations ADD CONSTRAINT fk_auth_cpt FOREIGN KEY (cpt_code_id) REFERENCES cpt_codes(cpt_id) ON DELETE SET NULL;

-- Foreign Keys for insurance_claims table
ALTER TABLE insurance_claims ADD CONSTRAINT fk_claim_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE insurance_claims ADD CONSTRAINT fk_claim_policy FOREIGN KEY (policy_id) REFERENCES patient_insurance_policies(policy_id) ON DELETE RESTRICT;
ALTER TABLE insurance_claims ADD CONSTRAINT fk_claim_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE CASCADE;

-- Foreign Keys for insurance_claim_items table
ALTER TABLE insurance_claim_items ADD CONSTRAINT fk_claim_item_claim FOREIGN KEY (claim_id) REFERENCES insurance_claims(claim_id) ON DELETE CASCADE;
ALTER TABLE insurance_claim_items ADD CONSTRAINT fk_claim_item_cpt FOREIGN KEY (cpt_code_id) REFERENCES cpt_codes(cpt_id) ON DELETE SET NULL;
ALTER TABLE insurance_claim_items ADD CONSTRAINT fk_claim_item_icd FOREIGN KEY (icd_code_id) REFERENCES icd_codes(icd_id) ON DELETE SET NULL;

-- Foreign Keys for invoices table
ALTER TABLE invoices ADD CONSTRAINT fk_invoice_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;
ALTER TABLE invoices ADD CONSTRAINT fk_invoice_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id) ON DELETE SET NULL;

-- Foreign Keys for invoice_items table
ALTER TABLE invoice_items ADD CONSTRAINT fk_item_invoice FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE;
ALTER TABLE invoice_items ADD CONSTRAINT fk_item_cpt FOREIGN KEY (cpt_code_id) REFERENCES cpt_codes(cpt_id) ON DELETE SET NULL;

-- Foreign Keys for payment_transactions table
ALTER TABLE payment_transactions ADD CONSTRAINT fk_payment_invoice FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE;
ALTER TABLE payment_transactions ADD CONSTRAINT fk_payment_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE;

-- Foreign Keys for user_roles table
ALTER TABLE user_roles ADD CONSTRAINT fk_user_role_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
ALTER TABLE user_roles ADD CONSTRAINT fk_user_role_role FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE;

-- =====================================================
-- Re-enable foreign key checks (all FKs created above)
-- =====================================================
SET FOREIGN_KEY_CHECKS=1;

-- =====================================================
-- DATABASE VIEWS
-- =====================================================


SELECT 'Hospital OLTP System schema (DDL) created successfully!' AS status;
