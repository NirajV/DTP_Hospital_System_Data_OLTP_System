"""
Hospital OLTP System - Comprehensive Fake Data Loader
======================================================

This script loads comprehensive fake data for the entire hospital OLTP system.
It loads data in dependency order to maintain PK-FK relationships:

Load Order:
1. Reference Data (ICD codes, CPT codes, appointments, insurance, medications, interactions)
2. Organizational Data (departments, facilities, rooms, beds)
3. Staff Data (doctors, nurses, general staff)
4. Patient Data (patients, addresses, emergency contacts)
5. Transactional Data (appointments, encounters, clinical data)

All data is realistic hospital data that maintains referential integrity.

Usage:
    python load_all_fake_data.py
    
    Or run individual loaders:
    python load_reference_data.py
    python load_organizational_data.py
    etc.

Exit Codes:
    0: All data loaded successfully
    1: One or more loading steps failed
"""

import mysql.connector
from mysql.connector import Error
import logging
import sys
import os
from datetime import datetime, timedelta
import random
from database_connection import DB_CONFIG, DATABASE_NAME, logger

# Suppress other loggers
logging.getLogger('mysql.connector').setLevel(logging.CRITICAL)


def setup_fake_data_log():
    """Create a per-run log file under Fake_Data_Log and attach it to logger."""
    log_dir = os.path.join(os.path.dirname(__file__), "Fake_Data_Log")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"load_all_fake_data_{timestamp}.log")

    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            if os.path.abspath(handler.baseFilename) == os.path.abspath(log_path):
                return log_path

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return log_path


def load_reference_data(cursor):
    """Load reference data layer"""
    print("\n[1/5] Loading Reference Data (ICD codes, CPT codes, etc.)...")
    
    # ICD Codes
    icd_data = [
        ('ICD-10', 'I10', 'Essential (primary) hypertension', 'Circulatory'),
        ('ICD-10', 'E11.9', 'Type 2 diabetes mellitus without complications', 'Endocrine'),
        ('ICD-10', 'J45.909', 'Unspecified asthma, uncomplicated', 'Respiratory'),
        ('ICD-10', 'M79.3', 'Panniculitis, unspecified', 'Musculoskeletal'),
        ('ICD-10', 'R51', 'Headache', 'Symptoms'),
        ('ICD-10', 'J06.9', 'Acute upper respiratory infection, unspecified', 'Respiratory'),
        ('ICD-10', 'K21.9', 'Gastro-esophageal reflux disease without esophagitis', 'Digestive'),
        ('ICD-10', 'I50.9', 'Heart failure, unspecified', 'Circulatory'),
        ('ICD-10', 'M19.0', 'Primary osteoarthritis of knee', 'Musculoskeletal'),
        ('ICD-10', 'E03.9', 'Hypothyroidism, unspecified', 'Endocrine'),
    ]
    
    sql = "INSERT IGNORE INTO icd_codes (icd_version, code, description, category) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, icd_data)
    logger.info(f"Loaded {cursor.rowcount} ICD codes")
    
    # CPT Codes
    cpt_data = [
        ('99213', 'Office/outpatient visit, established patient, 20-29 minutes', 'E/M', 1.50),
        ('99214', 'Office/outpatient visit, established patient, 30-39 minutes', 'E/M', 2.10),
        ('80053', 'Comprehensive metabolic panel', 'Lab', 0.75),
        ('85025', 'Complete blood count with differential', 'Lab', 0.50),
        ('71045', 'Chest X-ray, 2 views', 'Radiology', 1.20),
        ('93000', 'Electrocardiogram, routine ECG', 'Cardiology', 0.60),
        ('99203', 'Office visit, new patient, 30-39 minutes', 'E/M', 1.80),
        ('47562', 'Laparoscopic cholecystectomy', 'Surgery', 8.50),
        ('50200', 'Renal biopsy, percutaneous', 'Surgery', 3.20),
        ('76700', 'Abdominal ultrasound, B-scan', 'Radiology', 2.50),
    ]
    
    sql = "INSERT IGNORE INTO cpt_codes (code, description, category, relative_value) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, cpt_data)
    logger.info(f"Loaded {cursor.rowcount} CPT codes")
    
    # Appointment Types
    appointment_types = [
        ('Initial Consultation', 'First visit with a new patient', 45),
        ('Follow-up', 'Follow-up visit for existing condition', 30),
        ('Annual Physical', 'Annual checkup', 60),
        ('Emergency', 'Emergency appointment', 30),
        ('Procedure', 'Medical procedure appointment', 90),
        ('Lab Test', 'Laboratory testing', 20),
        ('Vaccination', 'Immunization appointment', 20),
        ('Post-Operative', 'Post-op follow-up', 30),
        ('Urgent Care', 'Urgent care visit', 30),
        ('Screening', 'Health screening', 45),
    ]
    
    sql = "INSERT IGNORE INTO appointment_types (type_name, description, default_duration) VALUES (%s, %s, %s)"
    cursor.executemany(sql, appointment_types)
    logger.info(f"Loaded {cursor.rowcount} appointment types")
    
    # Insurance Companies
    insurance_companies = [
        ('Blue Cross Blue Shield', 'BCBS', '1-800-555-0001', 'claims@bcbs.com', True),
        ('UnitedHealthcare', 'UHC', '1-800-555-0002', 'claims@uhc.com', True),
        ('Aetna', 'AETNA', '1-800-555-0003', 'claims@aetna.com', True),
        ('Cigna', 'CIGNA', '1-800-555-0004', 'claims@cigna.com', True),
        ('Anthem', 'ANTHEM', '1-800-555-0005', 'claims@anthem.com', True),
        ('Humana', 'HUMANA', '1-800-555-0006', 'claims@humana.com', True),
        ('Kaiser Permanente', 'KAISER', '1-800-555-0007', 'claims@kaiser.com', True),
        ('Medica', 'MEDICA', '1-800-555-0008', 'claims@medica.com', True),
        ('Friday Health Plans', 'FRIDAY', '1-800-555-0009', 'claims@friday.com', True),
        ('Molina Healthcare', 'MOLINA', '1-800-555-0010', 'claims@molina.com', True),
    ]
    
    sql = "INSERT IGNORE INTO insurance_companies (company_name, company_code, phone, email, is_active) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, insurance_companies)
    logger.info(f"Loaded {cursor.rowcount} insurance companies")
    
    # Medications
    medications = [
        ('Lisinopril', 'Lisinopril', 'ACE Inhibitor', '60505-2685-1', 'tablet', '10mg', 'Apotex', True, 12.50, 'active'),
        ('Metformin', 'Metformin HCl', 'Biguanide', '60505-0144-1', 'tablet', '500mg', 'Apotex', True, 8.75, 'active'),
        ('Amoxicillin', 'Amoxicillin', 'Antibiotic', '60505-0229-1', 'capsule', '500mg', 'Teva', True, 15.00, 'active'),
        ('Ibuprofen', 'Ibuprofen', 'NSAID', '60505-0121-1', 'tablet', '200mg', 'Major', False, 5.50, 'active'),
        ('Prednisone', 'Prednisone', 'Corticosteroid', '60505-0455-1', 'tablet', '20mg', 'Roxane', True, 10.00, 'active'),
        ('Sertraline', 'Sertraline HCl', 'SSRI', '60505-0158-1', 'tablet', '50mg', 'Apotex', True, 9.75, 'active'),
        ('Aspirin', 'Acetylsalicylic Acid', 'Antiplatelet', '60505-3580-1', 'tablet', '325mg', 'Bayer', False, 6.50, 'active'),
        ('Warfarin', 'Warfarin Sodium', 'Anticoagulant', '60505-0139-1', 'tablet', '5mg', 'Apotex', True, 8.00, 'active'),
        ('Albuterol', 'Albuterol Sulfate', 'Beta-2 Agonist', '60505-0134-1', 'inhaler', '90mcg', 'Apotex', True, 45.00, 'active'),
        ('Levothyroxine', 'Levothyroxine Sodium', 'Thyroid', '60505-0115-1', 'tablet', '75mcg', 'Apotex', True, 9.00, 'active'),
    ]
    
    sql = "INSERT IGNORE INTO medications (medication_name, generic_name, drug_class, ndc_code, dosage_form, strength, manufacturer, requires_prescription, unit_price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, medications)
    logger.info(f"Loaded {cursor.rowcount} medications")
    
    print("   [OK] Reference data loaded successfully")
    return True


def load_organizational_data(cursor):
    """Load organizational data (departments, facilities, rooms, beds, equipment)"""
    print("\n[2/5] Loading Organizational Data (departments, facilities, rooms, beds, equipment)...")
    
    # Load Departments (Enhanced)
    departments = [
        ('Cardiology', 'CARD', 'Cardiac care and heart disease treatment', 'Building A, Floor 3', '555-0101', 'cardiology@hospital.com', 'active'),
        ('Neurology', 'NEUR', 'Brain and nervous system treatment', 'Building A, Floor 4', '555-0102', 'neurology@hospital.com', 'active'),
        ('Pediatrics', 'PEDI', 'Children and infant care', 'Building B, Floor 1', '555-0103', 'pediatrics@hospital.com', 'active'),
        ('Emergency', 'EMER', 'Emergency and urgent care', 'Building C, Ground', '555-0105', 'emergency@hospital.com', 'active'),
        ('Radiology', 'RADI', 'Medical imaging', 'Building A, Floor 1', '555-0106', 'radiology@hospital.com', 'active'),
        ('Surgery', 'SURG', 'Surgical procedures and operating rooms', 'Building A, Floor 2', '555-0107', 'surgery@hospital.com', 'active'),
        ('Orthopedics', 'ORTH', 'Bone and joint treatment', 'Building B, Floor 2', '555-0108', 'orthopedics@hospital.com', 'active'),
        ('Oncology', 'ONCO', 'Cancer treatment and chemotherapy', 'Building D, Floor 1', '555-0109', 'oncology@hospital.com', 'active'),
        ('ICU', 'ICU', 'Intensive Care Unit', 'Building A, Floor 5', '555-0110', 'icu@hospital.com', 'active'),
        ('Obstetrics & Gynecology', 'OBG', 'Maternal and women health', 'Building B, Floor 3', '555-0111', 'obgyn@hospital.com', 'active'),
    ]
    
    sql = "INSERT IGNORE INTO departments (department_name, department_code, description, location, phone, email, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, departments)
    logger.info(f"Loaded {cursor.rowcount} department records")
    
    # Load Facilities (Buildings and physical structures)
    facilities = [
        ('Medical Center Building A', 'building', '500 Main Street, Healthcare City, ST 12345', 250, 'active'),
        ('Medical Center Building B', 'building', '501 Main Street, Healthcare City, ST 12345', 180, 'active'),
        ('Medical Center Building C', 'building', '502 Main Street, Healthcare City, ST 12345', 120, 'active'),
        ('Medical Center Building D', 'building', '503 Main Street, Healthcare City, ST 12345', 90, 'active'),
    ]
    
    sql = "INSERT IGNORE INTO facilities (facility_name, facility_type, address, total_capacity, status) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, facilities)
    logger.info(f"Loaded {cursor.rowcount} facility records")
    
    # Get facility and department IDs for relationships
    cursor.execute("SELECT facility_id FROM facilities ORDER BY facility_id LIMIT 4")
    facility_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT department_id FROM departments ORDER BY department_id LIMIT 10")
    dept_ids = [row[0] for row in cursor.fetchall()]
    
    # Load Rooms (Individual rooms linked to facilities and departments)
    rooms = []
    if facility_ids and dept_ids:
        # Building A Rooms
        rooms.extend([
            (facility_ids[0], dept_ids[0], '301A', 'patient', 3, 1, True, 'available'),
            (facility_ids[0], dept_ids[0], '301B', 'patient', 3, 1, True, 'available'),
            (facility_ids[0], dept_ids[0], '302A', 'patient', 3, 1, True, 'available'),
            (facility_ids[0], dept_ids[5], '201A', 'operating', 2, 1, True, 'available'),
            (facility_ids[0], dept_ids[5], '201B', 'operating', 2, 1, True, 'available'),
            (facility_ids[0], dept_ids[4], '101A', 'radiology', 1, 1, True, 'available'),
            (facility_ids[0], dept_ids[8], '501A', 'ICU', 5, 2, True, 'available'),
            (facility_ids[0], dept_ids[8], '502A', 'ICU', 5, 2, True, 'available'),
        ])
        # Building B Rooms
        rooms.extend([
            (facility_ids[1], dept_ids[2], '101A', 'patient', 1, 1, True, 'available'),
            (facility_ids[1], dept_ids[2], '101B', 'patient', 1, 1, True, 'available'),
            (facility_ids[1], dept_ids[2], '102A', 'patient', 1, 1, True, 'available'),
            (facility_ids[1], dept_ids[6], '202A', 'patient', 2, 1, True, 'available'),
            (facility_ids[1], dept_ids[9], '303A', 'examination', 3, 1, True, 'available'),
            (facility_ids[1], dept_ids[9], '304A', 'patient', 3, 2, True, 'available'),
        ])
        # Building C Rooms
        rooms.extend([
            (facility_ids[2], dept_ids[3], 'ER-01', 'ER', 0, 1, True, 'available'),
            (facility_ids[2], dept_ids[3], 'ER-02', 'ER', 0, 1, True, 'available'),
            (facility_ids[2], dept_ids[3], 'ER-03', 'ER', 0, 1, True, 'available'),
            (facility_ids[2], dept_ids[3], 'TRIAGE', 'examination', 0, 1, True, 'available'),
        ])
        # Building D Rooms
        rooms.extend([
            (facility_ids[3], dept_ids[7], 'CHEMO-01', 'patient', 1, 1, True, 'available'),
            (facility_ids[3], dept_ids[7], 'CHEMO-02', 'patient', 1, 1, True, 'available'),
            (facility_ids[3], dept_ids[7], 'INFUSION', 'patient', 1, 1, True, 'available'),
        ])
        
        sql = "INSERT IGNORE INTO rooms (facility_id, department_id, room_number, room_type, floor_number, capacity, is_available, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, rooms)
        logger.info(f"Loaded {cursor.rowcount} room records")
    
    # Get room IDs for bed creation
    cursor.execute("SELECT room_id FROM rooms ORDER BY room_id")
    room_ids = [row[0] for row in cursor.fetchall()]
    
    # Load Beds (Bed inventory linked to rooms)
    beds = []
    if room_ids:
        for room_idx, room_id in enumerate(room_ids):
            # Determine bed type based on room type
            if room_idx < 8:  # First 8 rooms are in ICU/patient rooms
                bed_type = 'ICU' if room_idx >= 6 else 'standard'
                num_beds = 2 if room_idx >= 6 else 1
            elif room_idx < 14:  # Next rooms in regular patient rooms
                bed_type = 'standard'
                num_beds = 1 if room_idx < 17 else 2
            else:  # ER and specialty rooms
                bed_type = 'standard'
                num_beds = 1
            
            for bed_num in range(1, num_beds + 1):
                beds.append((room_id, f'{chr(64+bed_num)}', bed_type, False, 'available'))
        
        sql = "INSERT IGNORE INTO beds (room_id, bed_number, bed_type, is_occupied, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql, beds)
        logger.info(f"Loaded {cursor.rowcount} bed records")
    
    # Load Equipment (Medical equipment)
    equipment = [
        ('Ventilator', 'Respiratory', 'Philips', 'V100', 'SN-V100-001', '2021-03-15', 45000.00, '2026-03-15', 'quarterly', '2025-10-01', '2026-01-15', 'available'),
        ('Patient Monitor', 'Monitoring', 'GE Healthcare', 'Carescape', 'SN-CS-001', '2020-06-20', 28000.00, '2025-06-20', 'semi-annual', '2025-09-01', '2026-03-01', 'available'),
        ('Infusion Pump', 'Infusion', 'Baxter', 'Colleague', 'SN-INF-001', '2022-01-10', 8500.00, '2027-01-10', 'annual', '2025-08-15', '2026-08-15', 'available'),
        ('IV Pole', 'Supply', 'Hill-Rom', 'Standard', 'SN-IVP-001', '2020-05-05', 500.00, '2025-05-05', 'annual', '2025-07-01', '2026-07-01', 'available'),
        ('Defibrillator', 'Emergency', 'Philips', 'Heartstart', 'SN-DEFI-001', '2021-11-12', 15000.00, '2026-11-12', 'annual', '2025-09-30', '2026-09-30', 'available'),
        ('Ultrasound Machine', 'Imaging', 'GE Healthcare', 'LOGIQ E10', 'SN-US-001', '2019-08-08', 80000.00, '2024-08-08', 'annual', '2025-06-01', '2026-06-01', 'available'),
        ('X-Ray System', 'Imaging', 'Siemens', 'AXIOM Luminos', 'SN-XR-001', '2018-04-14', 350000.00, '2023-04-14', 'annual', '2024-12-01', '2025-12-01', 'maintenance'),
        ('Operating Table', 'Surgery', 'Maquet', 'Alphamaxx', 'SN-OT-001', '2021-02-02', 120000.00, '2026-02-02', 'annual', '2025-07-15', '2026-07-15', 'available'),
        ('Surgical Lights', 'Surgery', 'Welch Allyn', 'Surgispot', 'SN-SL-001', '2020-09-09', 35000.00, '2025-09-09', 'annual', '2025-08-01', '2026-08-01', 'available'),
        ('Incubator', 'Pediatric', 'Dräger', 'Babylog', 'SN-INC-001', '2022-05-20', 25000.00, '2027-05-20', 'annual', '2025-09-01', '2026-09-01', 'available'),
        ('CT Scanner', 'Imaging', 'Philips', 'Brilliance', 'SN-CT-001', '2017-01-15', 500000.00, '2022-01-15', 'quarterly', '2024-11-01', '2025-02-01', 'maintenance'),
        ('MRI Machine', 'Imaging', 'Siemens', 'Magnetom', 'SN-MRI-001', '2016-10-20', 600000.00, '2021-10-20', 'quarterly', '2024-09-01', '2025-03-01', 'maintenance'),
    ]
    
    sql = "INSERT IGNORE INTO equipment (equipment_name, equipment_type, manufacturer, model_number, serial_number, purchase_date, purchase_cost, warranty_expiry, maintenance_schedule, last_maintenance, next_maintenance, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, equipment)
    logger.info(f"Loaded {cursor.rowcount} equipment records")
    
    # Get equipment IDs for department assignments
    cursor.execute("SELECT equipment_id FROM equipment ORDER BY equipment_id")
    equipment_ids = [row[0] for row in cursor.fetchall()]
    
    # Load Department Equipment Assignments
    dept_equipment = []
    if dept_ids and equipment_ids:
        # Assign equipment to departments based on type
        assignments = [
            (dept_ids[8], equipment_ids[0], '2024-01-15'),  # ICU gets ventilator
            (dept_ids[8], equipment_ids[1], '2024-01-10'),  # ICU gets patient monitor
            (dept_ids[5], equipment_ids[7], '2024-02-01'),  # Surgery gets operating table
            (dept_ids[5], equipment_ids[8], '2024-02-05'),  # Surgery gets surgical lights
            (dept_ids[4], equipment_ids[5], '2023-06-01'),  # Radiology gets ultrasound
            (dept_ids[4], equipment_ids[10], '2023-01-15'), # Radiology gets CT scanner
            (dept_ids[4], equipment_ids[11], '2022-10-20'), # Radiology gets MRI
            (dept_ids[3], equipment_ids[4], '2024-01-20'),  # Emergency gets defibrillator
            (dept_ids[2], equipment_ids[9], '2024-05-20'),  # Pediatrics gets incubator
            (dept_ids[0], equipment_ids[2], '2024-01-05'),  # Cardiology gets infusion pump
            (dept_ids[0], equipment_ids[3], '2024-01-01'),  # Cardiology gets IV pole
            (dept_ids[1], equipment_ids[3], '2024-01-08'),  # Neurology gets IV pole
        ]
        
        for dept_id, equip_id, assign_date in assignments:
            dept_equipment.append((dept_id, equip_id, assign_date, None, 'Equipment assigned to department'))
        
        sql = "INSERT IGNORE INTO department_equipment (department_id, equipment_id, assigned_date, return_date, notes) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql, dept_equipment)
        logger.info(f"Loaded {cursor.rowcount} department equipment assignment records")
    
    print("   [OK] Organizational data loaded successfully")
    return True


def load_staff_data(cursor):
    """Load comprehensive staff data (doctors, nurses, staff, specialists, assignments, shifts, schedules)"""
    print("\n[3/5] Loading Staff Data (doctors, nurses, staff, specialists, schedules)...")
    
    # Get department IDs
    cursor.execute("SELECT department_id FROM departments")
    dept_ids = [row[0] for row in cursor.fetchall()]
    
    if not dept_ids:
        logger.warning("No departments found; staff loading may have limited data")
        return True
    
    # Comprehensive Doctors (15 total - distributed across departments)
    doctors = [
        # Cardiology (2 doctors)
        ('DOC001', 'John', 'Smith', 'Cardiology', 'Interventional Cardiology', dept_ids[0], '555-1001', 'j.smith@hospital.com', 'LIC-001', 'CA', '2026-03-15', 'Board Certified - Cardiology', 'Johns Hopkins', 2005, 'NPI001', '2015-03-15', 250.00, 'active'),
        ('DOC002', 'Victoria', 'Chen', 'Cardiology', 'Heart Failure Specialist', dept_ids[0] if len(dept_ids) > 1 else dept_ids[0], '555-1002', 'v.chen@hospital.com', 'LIC-002', 'CA', '2026-05-20', 'Board Certified - Cardiology', 'Stanford Medical', 2006, 'NPI002', '2016-05-20', 240.00, 'active'),
        
        # Neurology (2 doctors)
        ('DOC003', 'Sarah', 'Johnson', 'Neurology', 'Stroke Specialist', dept_ids[1] if len(dept_ids) > 1 else dept_ids[0], '555-1003', 's.johnson@hospital.com', 'LIC-003', 'CA', '2025-07-20', 'Board Certified - Neurology', 'Harvard Medical', 2010, 'NPI003', '2016-07-20', 220.00, 'active'),
        ('DOC004', 'Marcus', 'Williams', 'Neurology', 'Epilepsy Specialist', dept_ids[1] if len(dept_ids) > 1 else dept_ids[0], '555-1004', 'm.williams@hospital.com', 'LIC-004', 'CA', '2025-09-15', 'Board Certified - Neurology', 'Yale Medical', 2008, 'NPI004', '2017-09-15', 210.00, 'active'),
        
        # Pediatrics (2 doctors)
        ('DOC005', 'Catherine', 'Brown', 'Pediatrics', 'General Pediatrics', dept_ids[2] if len(dept_ids) > 2 else dept_ids[0], '555-1005', 'c.brown@hospital.com', 'LIC-005', 'CA', '2026-01-10', 'Board Certified - Pediatrics', 'Boston Children Hospital', 2009, 'NPI005', '2017-01-10', 180.00, 'active'),
        ('DOC006', 'David', 'Garcia', 'Pediatrics', 'Pediatric Cardiology', dept_ids[2] if len(dept_ids) > 2 else dept_ids[0], '555-1006', 'd.garcia@hospital.com', 'LIC-006', 'CA', '2026-04-12', 'Board Certified - Pediatric Cardiology', 'UCSF Medical', 2011, 'NPI006', '2018-04-12', 200.00, 'active'),
        
        # Emergency (2 doctors)
        ('DOC007', 'Emily', 'Martinez', 'Emergency', 'Emergency Medicine', dept_ids[3] if len(dept_ids) > 3 else dept_ids[0], '555-1007', 'e.martinez@hospital.com', 'LIC-007', 'CA', '2024-05-12', 'Board Certified - Emergency', 'UCLA Medical', 2013, 'NPI007', '2018-05-12', 200.00, 'active'),
        ('DOC008', 'James', 'Taylor', 'Emergency', 'Trauma Specialist', dept_ids[3] if len(dept_ids) > 3 else dept_ids[0], '555-1008', 'j.taylor@hospital.com', 'LIC-008', 'CA', '2025-08-20', 'Board Certified - Emergency', 'UCSF Trauma', 2007, 'NPI008', '2015-08-20', 210.00, 'active'),
        
        # Radiology (2 doctors)
        ('DOC009', 'Patricia', 'Davis', 'Radiology', 'Diagnostic Radiology', dept_ids[4] if len(dept_ids) > 4 else dept_ids[0], '555-1009', 'p.davis@hospital.com', 'LIC-009', 'CA', '2026-04-20', 'Board Certified - Radiology', 'Mayo Clinic', 2006, 'NPI009', '2016-04-20', 225.00, 'active'),
        ('DOC010', 'Robert', 'Anderson', 'Radiology', 'Interventional Radiology', dept_ids[4] if len(dept_ids) > 4 else dept_ids[0], '555-1010', 'r.anderson@hospital.com', 'LIC-010', 'CA', '2025-06-15', 'Board Certified - Interventional Radiology', 'Johns Hopkins', 2005, 'NPI010', '2015-06-15', 240.00, 'active'),
        
        # Surgery (2 doctors)
        ('DOC011', 'Charles', 'Wilson', 'Surgery', 'General Surgery', dept_ids[5] if len(dept_ids) > 5 else dept_ids[0], '555-1011', 'c.wilson@hospital.com', 'LIC-011', 'CA', '2025-06-01', 'Board Certified - Surgery', 'UCSF Medical', 2004, 'NPI011', '2014-06-01', 280.00, 'active'),
        ('DOC012', 'Angela', 'Harris', 'Surgery', 'Vascular Surgery', dept_ids[5] if len(dept_ids) > 5 else dept_ids[0], '555-1012', 'a.harris@hospital.com', 'LIC-012', 'CA', '2026-02-10', 'Board Certified - Vascular Surgery', 'Stanford Medical', 2008, 'NPI012', '2017-02-10', 260.00, 'active'),
        
        # Oncology (1 doctor)
        ('DOC013', 'Richard', 'Lee', 'Oncology', 'Medical Oncology', dept_ids[7] if len(dept_ids) > 7 else dept_ids[0], '555-1013', 'r.lee@hospital.com', 'LIC-013', 'CA', '2025-03-15', 'Board Certified - Oncology', 'Dana-Farber', 2007, 'NPI013', '2016-03-15', 230.00, 'active'),
        
        # ICU (1 doctor)
        ('DOC014', 'Laura', 'Thomas', 'ICU', 'Critical Care Medicine', dept_ids[8] if len(dept_ids) > 8 else dept_ids[0], '555-1014', 'l.thomas@hospital.com', 'LIC-014', 'CA', '2025-08-20', 'Board Certified - Critical Care', 'Harvard Medical', 2009, 'NPI014', '2017-08-20', 245.00, 'active'),
        
        # OBG (1 doctor)
        ('DOC015', 'Susan', 'Garcia', 'Obstetrics & Gynecology', 'OB/GYN', dept_ids[9] if len(dept_ids) > 9 else dept_ids[0], '555-1015', 's.garcia@hospital.com', 'LIC-015', 'CA', '2025-10-05', 'Board Certified - OB/GYN', 'UCSF Medical', 2008, 'NPI015', '2016-10-05', 210.00, 'active'),
    ]
    
    sql = "INSERT IGNORE INTO doctors (employee_id, first_name, last_name, specialization, sub_specialization, department_id, phone, email, license_number, license_state, license_expiry, board_certification, medical_school, graduation_year, npi_number, hire_date, consultation_fee, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, doctors)
    logger.info(f"Loaded {cursor.rowcount} doctor records")
    
    # Get doctor IDs for specialists
    cursor.execute("SELECT doctor_id FROM doctors ORDER BY doctor_id")
    doctor_ids = [row[0] for row in cursor.fetchall()]
    
    # Load Specialists (Consulting doctors - select from doctors list)
    specialists = []
    if len(doctor_ids) >= 8:
        specialist_data = [
            (doctor_ids[0], 'Interventional Cardiology', 'Expertise in catheter-based interventions', 18, True),
            (doctor_ids[1], 'Heart Failure Management', 'Specialized in advanced heart failure therapies', 16, True),
            (doctor_ids[2], 'Stroke Neurology', 'Comprehensive stroke care and prevention', 15, True),
            (doctor_ids[3], 'Epilepsy Management', 'Advanced epilepsy treatment and EEG monitoring', 14, True),
            (doctor_ids[7], 'Trauma Surgery', 'Complex trauma and acute surgical care', 16, True),
            (doctor_ids[8], 'Interventional Radiology', 'Minimally invasive image-guided procedures', 17, True),
            (doctor_ids[11], 'Vascular Surgery', 'Vascular disease and limb salvage', 15, True),
            (doctor_ids[12], 'Chemotherapy Management', 'Personalized cancer treatment planning', 16, True),
        ]
        
        sql = "INSERT IGNORE INTO specialists (doctor_id, specialty_area, certification_details, years_of_experience, available_for_consultation) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql, specialist_data)
        logger.info(f"Loaded {cursor.rowcount} specialist records")
    
    # Comprehensive Nurses (15 total - distributed across departments)
    nurses = [
        # Cardiology (2 nurses)
        ('NUR001', 'Lisa', 'Anderson', dept_ids[0], 'RN-001', 'RN', '555-2001', 'l.anderson@hospital.com', '2017-06-01', 'day', 'active'),
        ('NUR002', 'Jennifer', 'Martinez', dept_ids[0] if len(dept_ids) > 1 else dept_ids[0], 'RN-002', 'RN', '555-2002', 'j.martinez@hospital.com', '2018-09-15', 'rotating', 'active'),
        
        # Neurology (2 nurses)
        ('NUR003', 'James', 'Taylor', dept_ids[1] if len(dept_ids) > 1 else dept_ids[0], 'RN-003', 'RN', '555-2003', 'j.taylor@hospital.com', '2018-03-15', 'night', 'active'),
        ('NUR004', 'Amanda', 'Wilson', dept_ids[1] if len(dept_ids) > 1 else dept_ids[0], 'RN-004', 'RN', '555-2004', 'a.wilson@hospital.com', '2019-05-20', 'day', 'active'),
        
        # Pediatrics (2 nurses)
        ('NUR005', 'Maria', 'Rodriguez', dept_ids[2] if len(dept_ids) > 2 else dept_ids[0], 'RN-005', 'RN', '555-2005', 'm.rodriguez@hospital.com', '2019-01-10', 'rotating', 'active'),
        ('NUR006', 'Michelle', 'Davis', dept_ids[2] if len(dept_ids) > 2 else dept_ids[0], 'LPN-001', 'LPN', '555-2006', 'm.davis@hospital.com', '2020-03-01', 'day', 'active'),
        
        # Emergency (2 nurses)
        ('NUR007', 'William', 'Lee', dept_ids[3] if len(dept_ids) > 3 else dept_ids[0], 'RN-006', 'RN', '555-2007', 'w.lee@hospital.com', '2017-09-20', 'rotating', 'active'),
        ('NUR008', 'Rachel', 'Thompson', dept_ids[3] if len(dept_ids) > 3 else dept_ids[0], 'RN-007', 'RN', '555-2008', 'r.thompson@hospital.com', '2018-07-15', 'night', 'active'),
        
        # Radiology (2 nurses)
        ('NUR009', 'Patricia', 'Harris', dept_ids[4] if len(dept_ids) > 4 else dept_ids[0], 'RN-008', 'RN', '555-2009', 'p.harris@hospital.com', '2016-11-01', 'day', 'active'),
        ('NUR010', 'Kevin', 'Jackson', dept_ids[4] if len(dept_ids) > 4 else dept_ids[0], 'RN-009', 'RN', '555-2010', 'k.jackson@hospital.com', '2019-02-15', 'rotating', 'active'),
        
        # Surgery (2 nurses)
        ('NUR011', 'Susan', 'Clark', dept_ids[5] if len(dept_ids) > 5 else dept_ids[0], 'RN-010', 'RN', '555-2011', 's.clark@hospital.com', '2017-04-01', 'day', 'active'),
        ('NUR012', 'Daniel', 'White', dept_ids[5] if len(dept_ids) > 5 else dept_ids[0], 'RN-011', 'RN', '555-2012', 'd.white@hospital.com', '2018-06-15', 'rotating', 'active'),
        
        # ICU (2 nurses)
        ('NUR013', 'Donna', 'Green', dept_ids[8] if len(dept_ids) > 8 else dept_ids[0], 'RN-012', 'RN', '555-2013', 'd.green@hospital.com', '2016-08-20', 'rotating', 'active'),
        ('NUR014', 'Thomas', 'Moore', dept_ids[8] if len(dept_ids) > 8 else dept_ids[0], 'RN-013', 'RN', '555-2014', 't.moore@hospital.com', '2017-10-01', 'night', 'active'),
        
        # OBG (1 nurse)
        ('NUR015', 'Rebecca', 'Brown', dept_ids[9] if len(dept_ids) > 9 else dept_ids[0], 'RN-014', 'RN', '555-2015', 'r.brown@hospital.com', '2019-07-10', 'day', 'active'),
    ]
    
    sql = "INSERT IGNORE INTO nurses (employee_id, first_name, last_name, department_id, license_number, license_type, phone, email, hire_date, shift_preference, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, nurses)
    logger.info(f"Loaded {cursor.rowcount} nurse records")
    
    # Get nurse IDs for assignments
    cursor.execute("SELECT nurse_id FROM nurses ORDER BY nurse_id")
    nurse_ids = [row[0] for row in cursor.fetchall()]
    
    # Get patient IDs for nurse assignments
    cursor.execute("SELECT patient_id FROM patients ORDER BY patient_id")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    # Get bed IDs for nurse assignments
    cursor.execute("SELECT bed_id FROM beds ORDER BY bed_id LIMIT 15")
    bed_ids = [row[0] for row in cursor.fetchall()]
    
    # Load Nurse Assignments (Assign nurses to patients)
    if nurse_ids and patient_ids:
        base_date = datetime(2024, 1, 15)
        assignment_data = []
        
        # Create assignments for available nurses and patients (safely)
        num_assignments = min(len(nurse_ids), len(patient_ids), 15)
        shift_types = ['day', 'evening', 'night']
        
        for i in range(num_assignments):
            assignment_data.append((
                nurse_ids[i],
                patient_ids[i],
                bed_ids[i] if i < len(bed_ids) else None,
                base_date + timedelta(days=i % 7),
                None,
                shift_types[i % len(shift_types)],
                f'Nurse assignment {i+1}'
            ))
        
        if assignment_data:
            sql = "INSERT IGNORE INTO nurse_assignments (nurse_id, patient_id, bed_id, assigned_date, end_date, shift, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, assignment_data)
            logger.info(f"Loaded {cursor.rowcount} nurse assignment records")
    
    # Administrative Staff (8 staff members)
    staff = [
        ('STF001', 'Robert', 'Johnson', dept_ids[0], 'Department Manager', '555-3001', 'r.johnson@hospital.com', '2015-01-15', None, 95000.00, 'active'),
        ('STF002', 'Carol', 'Williams', dept_ids[1] if len(dept_ids) > 1 else dept_ids[0], 'Clinical Coordinator', '555-3002', 'c.williams@hospital.com', '2016-03-20', None, 65000.00, 'active'),
        ('STF003', 'Michael', 'Brown', dept_ids[3] if len(dept_ids) > 3 else dept_ids[0], 'ER Coordinator', '555-3003', 'm.brown@hospital.com', '2017-06-15', None, 70000.00, 'active'),
        ('STF004', 'Jessica', 'Davis', dept_ids[5] if len(dept_ids) > 5 else dept_ids[0], 'Surgical Coordinator', '555-3004', 'j.davis@hospital.com', '2016-08-01', None, 72000.00, 'active'),
        ('STF005', 'David', 'Miller', dept_ids[4] if len(dept_ids) > 4 else dept_ids[0], 'Radiology Technician Lead', '555-3005', 'd.miller@hospital.com', '2017-02-10', None, 68000.00, 'active'),
        ('STF006', 'Sandra', 'Garcia', dept_ids[8] if len(dept_ids) > 8 else dept_ids[0], 'ICU Coordinator', '555-3006', 's.garcia@hospital.com', '2016-11-05', None, 75000.00, 'active'),
        ('STF007', 'Richard', 'Rodriguez', dept_ids[7] if len(dept_ids) > 7 else dept_ids[0], 'Oncology Administrator', '555-3007', 'r.rodriguez@hospital.com', '2018-04-15', None, 70000.00, 'active'),
        ('STF008', 'Linda', 'Martinez', dept_ids[9] if len(dept_ids) > 9 else dept_ids[0], 'OBG Administrator', '555-3008', 'l.martinez@hospital.com', '2017-09-20', None, 68000.00, 'active'),
    ]
    
    sql = "INSERT IGNORE INTO staff (employee_id, first_name, last_name, department_id, position, phone, email, hire_date, termination_date, salary, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, staff)
    logger.info(f"Loaded {cursor.rowcount} staff records")
    
    # Get staff IDs for shift scheduling
    cursor.execute("SELECT staff_id FROM staff ORDER BY staff_id")
    staff_ids = [row[0] for row in cursor.fetchall()]
    
    # Load Staff Shifts (Varied shifts for staff and nurses)
    shifts = []
    shift_types = ['morning', 'afternoon', 'evening', 'night', 'overnight']
    start_time_map = {'morning': '08:00:00', 'afternoon': '12:00:00', 'evening': '16:00:00', 'night': '20:00:00', 'overnight': '00:00:00'}
    end_time_map = {'morning': '16:00:00', 'afternoon': '20:00:00', 'evening': '00:00:00', 'night': '04:00:00', 'overnight': '08:00:00'}
    
    base_shift_date = datetime(2024, 3, 1)
    
    if staff_ids:
        for staff_idx, staff_id in enumerate(staff_ids[:8]):
            for day_offset in range(7):
                shift_type = shift_types[day_offset % len(shift_types)]
                shift_date = base_shift_date + timedelta(days=day_offset)
                shifts.append((staff_id, None, shift_date.date(), shift_type, start_time_map[shift_type], end_time_map[shift_type], 'scheduled', 'Regular shift'))
    
    if nurse_ids:
        for nurse_idx, nurse_id in enumerate(nurse_ids[:10]):
            for day_offset in range(7):
                shift_type = shift_types[day_offset % len(shift_types)]
                shift_date = base_shift_date + timedelta(days=day_offset)
                shifts.append((None, nurse_id, shift_date.date(), shift_type, start_time_map[shift_type], end_time_map[shift_type], 'scheduled', f'Nurse shift - {shift_type}'))
    
    if shifts:
        sql = "INSERT IGNORE INTO staff_shifts (staff_id, nurse_id, shift_date, shift_type, start_time, end_time, status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, shifts)
        logger.info(f"Loaded {cursor.rowcount} staff shift records")
    
    # Load Doctor Schedules (Weekly availability)
    schedules = []
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    if doctor_ids:
        for doc_idx, doctor_id in enumerate(doctor_ids):
            # Each doctor has a pattern of available days
            available_days = days_of_week if doc_idx % 2 == 0 else days_of_week[:5]  # Some doctors work weekends
            
            for day in available_days:
                if day in ['Saturday', 'Sunday']:
                    # Weekend doctors have different hours
                    schedules.append((doctor_id, day, '10:00:00', '14:00:00', None, 20, True, None, None))
                else:
                    # Weekday hours vary
                    if doc_idx % 3 == 0:
                        schedules.append((doctor_id, day, '08:00:00', '16:00:00', None, 25, True, None, None))
                    elif doc_idx % 3 == 1:
                        schedules.append((doctor_id, day, '09:00:00', '17:00:00', None, 20, True, None, None))
                    else:
                        schedules.append((doctor_id, day, '10:00:00', '18:00:00', None, 15, True, None, None))
    
    if schedules:
        sql = "INSERT IGNORE INTO doctor_schedules (doctor_id, day_of_week, start_time, end_time, room_id, max_patients, is_active, effective_from, effective_to) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, schedules)
        logger.info(f"Loaded {cursor.rowcount} doctor schedule records")
    
    print("   [OK] Staff data loaded successfully")
    return True


def load_patient_data(cursor):
    """Load patient data (patients, addresses, emergency contacts, allergies)"""
    print("\n[4/5] Loading Patient Data (patients, addresses, contacts, allergies)...")
    
    # Comprehensive Patient Data (15 patients)
    patients = [
        # Cardiology patients
        ('MRN001', 'Alice', 'Anderson', '1945-05-15', 'Female', '123-45-6001', '555-4001', 'alice.anderson@email.com', 'A+', 'married', '2023-01-15', 'active'),
        ('MRN002', 'Robert', 'Taylor', '1960-08-22', 'Male', '123-45-6002', '555-4002', 'robert.taylor@email.com', 'B+', 'married', '2023-02-20', 'active'),
        
        # Neurology patients
        ('MRN003', 'Jennifer', 'Martinez', '1978-12-10', 'Female', '123-45-6003', '555-4003', 'jennifer.martinez@email.com', 'O+', 'single', '2023-03-10', 'active'),
        ('MRN004', 'William', 'Garcia', '2008-03-30', 'Male', '123-45-6004', '555-4004', 'william.garcia@email.com', 'AB+', 'single', '2023-04-05', 'active'),
        
        # Pediatrics patients
        ('MRN005', 'Lisa', 'Rodriguez', '2018-06-18', 'Female', '123-45-6005', '555-4005', 'lisa.rodriguez@email.com', 'O-', 'single', '2023-05-12', 'active'),
        ('MRN006', 'Michael', 'Johnson', '2010-09-25', 'Male', '123-45-6006', '555-4006', 'michael.johnson@email.com', 'B-', 'single', '2023-06-08', 'active'),
        
        # Emergency patients
        ('MRN007', 'Sarah', 'Williams', '1988-11-03', 'Female', '123-45-6007', '555-4007', 'sarah.williams@email.com', 'A-', 'divorced', '2023-07-14', 'active'),
        ('MRN008', 'Christopher', 'Brown', '1975-01-17', 'Male', '123-45-6008', '555-4008', 'christopher.brown@email.com', 'AB-', 'married', '2023-08-22', 'active'),
        
        # Radiology patients
        ('MRN009', 'Patricia', 'Davis', '1952-04-20', 'Female', '123-45-6009', '555-4009', 'patricia.davis@email.com', 'O+', 'widowed', '2023-09-11', 'active'),
        ('MRN010', 'James', 'Miller', '1942-07-08', 'Male', '123-45-6010', '555-4010', 'james.miller@email.com', 'B+', 'married', '2023-10-19', 'active'),
        
        # Oncology patients
        ('MRN011', 'Elizabeth', 'Wilson', '1960-02-14', 'Female', '123-45-6011', '555-4011', 'elizabeth.wilson@email.com', 'A+', 'single', '2023-11-05', 'active'),
        ('MRN012', 'David', 'Moore', '1970-10-30', 'Male', '123-45-6012', '555-4012', 'david.moore@email.com', 'O-', 'married', '2023-12-01', 'active'),
        
        # ICU patients
        ('MRN013', 'Nancy', 'Taylor', '1955-06-22', 'Female', '123-45-6013', '555-4013', 'nancy.taylor@email.com', 'B+', 'divorced', '2024-01-10', 'active'),
        ('MRN014', 'Daniel', 'Anderson', '1965-03-11', 'Male', '123-45-6014', '555-4014', 'daniel.anderson@email.com', 'AB+', 'married', '2024-02-15', 'active'),
        
        # OBG patient
        ('MRN015', 'Jessica', 'Thompson', '1992-08-19', 'Female', '123-45-6015', '555-4015', 'jessica.thompson@email.com', 'A+', 'married', '2024-03-20', 'active'),
    ]
    
    sql = "INSERT IGNORE INTO patients (mrn, first_name, last_name, date_of_birth, gender, ssn, phone, email, blood_group, marital_status, registration_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, patients)
    logger.info(f"Loaded {cursor.rowcount} patient records")
    
    # Get patient IDs for relationships
    cursor.execute("SELECT patient_id, first_name, last_name FROM patients ORDER BY patient_id")
    patient_data = cursor.fetchall()
    patient_ids = [row[0] for row in patient_data]
    
    if patient_ids:
        # Extended Patient Addresses (multiple addresses per patient where applicable)
        addresses = [
            # Alice Anderson - Cardiology
            (patient_ids[0], 'home', '123 Main St', 'Springfield', 'IL', '62701', True),
            (patient_ids[0], 'work', '543 Business Blvd', 'Springfield', 'IL', '62702', False),
            
            # Robert Taylor - Cardiology
            (patient_ids[1], 'home', '456 Oak Ave', 'Springfield', 'IL', '62702', True),
            
            # Jennifer Martinez - Neurology
            (patient_ids[2], 'home', '789 Pine Rd', 'Springfield', 'IL', '62703', True),
            (patient_ids[2], 'summer', '200 Beach Lane', 'Coastal City', 'FL', '32080', False),
            
            # William Garcia - Neurology
            (patient_ids[3], 'home', '321 Elm St', 'Springfield', 'IL', '62704', True),
            
            # Lisa Rodriguez - Pediatrics
            (patient_ids[4], 'home', '654 Maple Dr', 'Springfield', 'IL', '62705', True),
            
            # Michael Johnson - Pediatrics
            (patient_ids[5], 'home', '987 Cedar Lane', 'Springfield', 'IL', '62706', True),
            (patient_ids[5], 'school', '555 Academy Rd', 'Springfield', 'IL', '62707', False),
            
            # Sarah Williams - Emergency
            (patient_ids[6], 'home', '111 Birch St', 'Springfield', 'IL', '62708', True),
            
            # Christopher Brown - Emergency
            (patient_ids[7], 'home', '222 Spruce Ave', 'Springfield', 'IL', '62709', True),
            (patient_ids[7], 'work', '100 Corporate Dr', 'Springfield', 'IL', '62710', False),
            
            # Patricia Davis - Radiology
            (patient_ids[8], 'home', '333 Ash St', 'Springfield', 'IL', '62711', True),
            
            # James Miller - Radiology
            (patient_ids[9], 'home', '444 Walnut Rd', 'Springfield', 'IL', '62712', True),
            (patient_ids[9], 'retirement', '600 Golden Years Dr', 'Retirement City', 'FL', '32081', False),
            
            # Elizabeth Wilson - Oncology
            (patient_ids[10], 'home', '555 Chestnut Lane', 'Springfield', 'IL', '62713', True),
            
            # David Moore - Oncology
            (patient_ids[11], 'home', '666 Hickory Ave', 'Springfield', 'IL', '62714', True),
            (patient_ids[11], 'work', '750 Tech Park', 'Springfield', 'IL', '62715', False),
            
            # Nancy Taylor - ICU
            (patient_ids[12], 'home', '777 Sycamore St', 'Springfield', 'IL', '62716', True),
            
            # Daniel Anderson - ICU
            (patient_ids[13], 'home', '888 Magnolia Dr', 'Springfield', 'IL', '62717', True),
            
            # Jessica Thompson - OBG
            (patient_ids[14], 'home', '999 Laurel Ave', 'Springfield', 'IL', '62718', True),
            (patient_ids[14], 'work', '555 Medical Center', 'Springfield', 'IL', '62719', False),
        ]
        
        sql = "INSERT IGNORE INTO patient_addresses (patient_id, address_type, street_address1, city, state, postal_code, is_primary) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, addresses)
        logger.info(f"Loaded {cursor.rowcount} patient address records")
        
        # Comprehensive Emergency Contacts (multiple contacts per patient)
        contacts = [
            # Alice Anderson
            (patient_ids[0], 'Bob Anderson', 'Spouse', '555-4020', True),
            (patient_ids[0], 'Charles Anderson', 'Son', '555-4021', False),
            
            # Robert Taylor
            (patient_ids[1], 'Mary Taylor', 'Spouse', '555-4022', True),
            (patient_ids[1], 'Susan Taylor', 'Daughter', '555-4023', False),
            
            # Jennifer Martinez
            (patient_ids[2], 'Carlos Martinez', 'Spouse', '555-4024', True),
            (patient_ids[2], 'Rosa Martinez', 'Mother', '555-4025', False),
            
            # William Garcia
            (patient_ids[3], 'Linda Garcia', 'Mother', '555-4026', True),
            (patient_ids[3], 'Maria Garcia', 'Sister', '555-4027', False),
            
            # Lisa Rodriguez
            (patient_ids[4], 'James Rodriguez', 'Father', '555-4028', True),
            (patient_ids[4], 'Michelle Rodriguez', 'Mother', '555-4029', False),
            
            # Michael Johnson
            (patient_ids[5], 'Sarah Johnson', 'Mother', '555-4030', True),
            (patient_ids[5], 'Mark Johnson', 'Father', '555-4031', False),
            
            # Sarah Williams
            (patient_ids[6], 'John Williams', 'Brother', '555-4032', True),
            (patient_ids[6], 'Emma Williams', 'Sister', '555-4033', False),
            
            # Christopher Brown
            (patient_ids[7], 'Patricia Brown', 'Spouse', '555-4034', True),
            (patient_ids[7], 'Thomas Brown', 'Son', '555-4035', False),
            
            # Patricia Davis
            (patient_ids[8], 'George Davis', 'Brother', '555-4036', True),
            (patient_ids[8], 'Helen Davis', 'Daughter', '555-4037', False),
            
            # James Miller
            (patient_ids[9], 'Margaret Miller', 'Spouse', '555-4038', True),
            (patient_ids[9], 'Edward Miller', 'Son', '555-4039', False),
            
            # Elizabeth Wilson
            (patient_ids[10], 'Frank Wilson', 'Son', '555-4040', True),
            (patient_ids[10], 'Dorothy Wilson', 'Daughter', '555-4041', False),
            
            # David Moore
            (patient_ids[11], 'Catherine Moore', 'Spouse', '555-4042', True),
            (patient_ids[11], 'Andrew Moore', 'Son', '555-4043', False),
            
            # Nancy Taylor
            (patient_ids[12], 'Kenneth Taylor', 'Brother', '555-4044', True),
            (patient_ids[12], 'Sandra Taylor', 'Sister', '555-4045', False),
            
            # Daniel Anderson
            (patient_ids[13], 'Ruth Anderson', 'Spouse', '555-4046', True),
            (patient_ids[13], 'Paul Anderson', 'Son', '555-4047', False),
            
            # Jessica Thompson
            (patient_ids[14], 'Richard Thompson', 'Spouse', '555-4048', True),
            (patient_ids[14], 'Karen Thompson', 'Mother', '555-4049', False),
        ]
        
        sql = "INSERT IGNORE INTO patient_emergency_contacts (patient_id, contact_name, relationship, phone, is_primary) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql, contacts)
        logger.info(f"Loaded {cursor.rowcount} emergency contact records")
        
        # Comprehensive Patient Allergies (realistic medical allergies)
        allergies = [
            # Alice Anderson - Cardiology (Hypertension, Cardiac)
            (patient_ids[0], 'Penicillin', 'drug', 'Anaphylaxis, severe rash', 'life-threatening', '1995-03-10', 'Known penicillin allergy', 'active'),
            (patient_ids[0], 'Shellfish', 'food', 'Hives, angioedema', 'severe', '1985-06-15', 'Shellfish allergy', 'active'),
            
            # Robert Taylor - Cardiology
            (patient_ids[1], 'Aspirin', 'drug', 'GI bleeding, stomach upset', 'moderate', '2010-05-20', 'Aspirin sensitivity', 'active'),
            (patient_ids[1], 'Latex', 'environmental', 'Contact dermatitis', 'mild', '2005-08-30', 'Latex glove reaction', 'active'),
            
            # Jennifer Martinez - Neurology
            (patient_ids[2], 'Sulfonamides', 'drug', 'Stevens-Johnson syndrome', 'life-threatening', '2000-02-14', 'Severe sulfa allergy', 'active'),
            
            # William Garcia - Neurology
            (patient_ids[3], 'Amoxicillin', 'drug', 'Rash, itching', 'moderate', '2015-09-11', 'Amoxicillin rash', 'active'),
            (patient_ids[3], 'Peanuts', 'food', 'Anaphylaxis, throat swelling', 'life-threatening', '2008-04-22', 'Severe peanut allergy', 'active'),
            
            # Lisa Rodriguez - Pediatrics
            (patient_ids[4], 'Eggs', 'food', 'Itching, mild rash', 'mild', '2019-01-15', 'Egg allergy diagnosed', 'active'),
            (patient_ids[4], 'Cats', 'environmental', 'Asthma symptoms, wheezing', 'moderate', '2018-07-20', 'Cat allergy', 'active'),
            
            # Michael Johnson - Pediatrics
            (patient_ids[5], 'Peanuts', 'food', 'Anaphylaxis', 'life-threatening', '2012-03-08', 'EpiPen carrier', 'active'),
            (patient_ids[5], 'Dust mites', 'environmental', 'Asthma aggravation', 'moderate', '2011-09-14', 'Dust allergy', 'active'),
            
            # Sarah Williams - Emergency
            (patient_ids[6], 'Codeine', 'drug', 'Severe reaction, urticaria', 'severe', '2005-11-22', 'Codeine allergy', 'active'),
            (patient_ids[6], 'Tree nuts', 'food', 'Throat itching, swelling', 'moderate', '2010-05-30', 'Tree nut allergy', 'active'),
            
            # Christopher Brown - Emergency
            (patient_ids[7], 'NSAIDs', 'drug', 'GI upset, bleeding', 'moderate', '2008-03-18', 'NSAID sensitivity', 'active'),
            
            # Patricia Davis - Radiology
            (patient_ids[8], 'Iodine contrast', 'drug', 'Anaphylaxis, difficulty breathing', 'life-threatening', '2015-12-10', 'Contrast allergy - use non-ionic', 'active'),
            (patient_ids[8], 'Dairy', 'food', 'Lactose intolerance, GI issues', 'moderate', '1998-07-25', 'Dairy intolerance', 'active'),
            
            # James Miller - Radiology
            (patient_ids[9], 'Gadolinium contrast', 'drug', 'Nephrogenic systemic fibrosis risk', 'severe', '2018-01-20', 'Gadolinium allergy - use alternative', 'active'),
            
            # Elizabeth Wilson - Oncology
            (patient_ids[10], '5-Fluorouracil', 'drug', 'Hand-foot syndrome', 'severe', '2020-06-15', 'Chemotherapy reaction documented', 'active'),
            (patient_ids[10], 'Kiwi', 'food', 'Throat itching, oral allergy syndrome', 'moderate', '2012-08-22', 'Kiwi allergy', 'active'),
            
            # David Moore - Oncology
            (patient_ids[11], 'Cisplatin', 'drug', 'Severe nausea, neuropathy', 'severe', '2019-03-05', 'Cisplatin reaction', 'active'),
            (patient_ids[11], 'Alcohol', 'other', 'Severe flushing, headache', 'moderate', '2000-10-12', 'Disulfiram-like reaction', 'active'),
            
            # Nancy Taylor - ICU
            (patient_ids[12], 'Vancomycin', 'drug', 'Red man syndrome, flushing', 'moderate', '2018-05-28', 'Requires premedication', 'active'),
            
            # Daniel Anderson - ICU
            (patient_ids[13], 'Morphine', 'drug', 'Histamine release, itching', 'moderate', '2015-09-30', 'Use alternative opioids', 'active'),
            (patient_ids[13], 'Bee stings', 'environmental', 'Anaphylaxis', 'life-threatening', '1999-06-10', 'EpiPen carrier required', 'active'),
            
            # Jessica Thompson - OBG
            (patient_ids[14], 'Tetracycline', 'drug', 'Vaginal yeast infection', 'mild', '2018-04-15', 'Estrogen-related reaction', 'active'),
            (patient_ids[14], 'Bananas', 'food', 'Oral allergy syndrome only', 'mild', '2016-07-20', 'Mild reaction', 'active'),
        ]
        
        sql = "INSERT IGNORE INTO patient_allergies (patient_id, allergen_name, allergen_type, reaction, severity, onset_date, notes, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, allergies)
        logger.info(f"Loaded {cursor.rowcount} patient allergy records")
    
    print("   [OK] Patient data loaded successfully")
    return True


def load_transactional_data(cursor):
    """Load transactional data (appointments, encounters, clinical data)"""
    print("\n[5/5] Loading Transactional Data (appointments, encounters, clinical)...")
    
    # Get needed IDs for appointments
    cursor.execute("SELECT patient_id FROM patients")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT doctor_id FROM doctors")
    doctor_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT nurse_id FROM nurses")
    nurse_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT room_id FROM rooms")
    room_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT bed_id FROM beds")
    bed_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT department_id FROM departments")
    dept_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT icd_id FROM icd_codes")
    icd_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT cpt_id FROM cpt_codes")
    cpt_ids = [row[0] for row in cursor.fetchall()]
    
    # 1. Load Appointment Types (if not already loaded)
    cursor.execute("SELECT COUNT(*) FROM appointment_types")
    if cursor.fetchone()[0] == 0:
        appt_types = [
            ('Routine Checkup', 'Regular patient examination and health assessment', 30, '#0099FF', False, None),
            ('Follow-up Visit', 'Follow-up consultation for existing condition', 20, '#00CC00', False, None),
            ('New Patient', 'Initial consultation for new patient', 45, '#FF6600', True, 'Bring medical history and insurance cards'),
            ('Urgent Care', 'Acute medical issues requiring prompt attention', 30, '#FF0000', False, None),
            ('Surgery Consultation', 'Pre-surgical evaluation and planning', 60, '#9900CC', True, 'NPO 6 hours before appointment if considering surgery'),
            ('Lab Test', 'Laboratory test collection and procedures', 15, '#00FFCC', True, 'Fasting may be required - confirm with lab'),
            ('Imaging Study', 'Radiology or imaging procedures', 45, '#FF00FF', True, 'Remove metal objects; confirm contrast needs'),
            ('Physical Therapy', 'Physical rehabilitation and exercise', 45, '#999900', False, None),
            ('Mental Health', 'Psychiatric or psychological counseling', 50, '#FF99CC', False, None),
            ('Wellness Visit', 'Preventive care and wellness screening', 30, '#00FF99', False, None),
        ]
        
        sql = "INSERT IGNORE INTO appointment_types (type_name, description, default_duration, color_code, requires_preparation, preparation_instructions) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, appt_types)
        logger.info(f"Loaded {cursor.rowcount} appointment type records")
    
    cursor.execute("SELECT type_id FROM appointment_types")
    appt_type_ids = [row[0] for row in cursor.fetchall()]
    
    # 2. Load Appointments (comprehensive scheduling)
    if patient_ids and doctor_ids and appt_type_ids:
        base_date = datetime(2024, 3, 15)
        appointments = []
        
        # Create 25 appointments across different patients and doctors
        appointment_data = [
            # Cardiology appointments
            (patient_ids[0], doctor_ids[0], appt_type_ids[0], base_date, '09:00:00', 30, 'Annual cardiology checkup', 'completed', 'routine'),
            (patient_ids[0], doctor_ids[0], appt_type_ids[1], base_date + timedelta(days=30), '10:30:00', 20, 'Follow-up on hypertension control', 'scheduled', 'routine'),
            (patient_ids[1], doctor_ids[0], appt_type_ids[0], base_date + timedelta(days=2), '14:00:00', 30, 'Chest pain evaluation', 'completed', 'urgent'),
            
            # Neurology appointments
            (patient_ids[2], doctor_ids[1], appt_type_ids[2], base_date, '11:00:00', 45, 'New neurology patient - headaches', 'completed', 'routine'),
            (patient_ids[3], doctor_ids[1], appt_type_ids[0], base_date + timedelta(days=5), '09:30:00', 30, 'Seizure management review', 'completed', 'routine'),
            
            # Pediatrics appointments
            (patient_ids[4], doctor_ids[2], appt_type_ids[0], base_date + timedelta(days=1), '10:00:00', 20, 'Well child visit - 6 year old', 'completed', 'routine'),
            (patient_ids[5], doctor_ids[2], appt_type_ids[0], base_date + timedelta(days=3), '15:00:00', 30, 'Adolescent health screening', 'completed', 'routine'),
            
            # Emergency/Urgent appointments
            (patient_ids[6], doctor_ids[3], appt_type_ids[3], base_date + timedelta(days=0), '08:00:00', 30, 'Acute injury assessment', 'completed', 'urgent'),
            (patient_ids[7], doctor_ids[3], appt_type_ids[3], base_date + timedelta(days=2), '16:00:00', 20, 'Acute abdominal pain', 'completed', 'urgent'),
            
            # Radiology appointments
            (patient_ids[8], doctor_ids[4], appt_type_ids[6], base_date + timedelta(days=1), '13:00:00', 45, 'CT scan - chest imaging', 'completed', 'routine'),
            (patient_ids[9], doctor_ids[4], appt_type_ids[6], base_date + timedelta(days=4), '10:00:00', 30, 'Ultrasound - abdominal', 'completed', 'routine'),
            
            # Surgery consultation
            (patient_ids[10], doctor_ids[5], appt_type_ids[4], base_date, '11:30:00', 60, 'Pre-operative surgery consultation', 'completed', 'routine'),
            (patient_ids[11], doctor_ids[5], appt_type_ids[0], base_date + timedelta(days=7), '09:00:00', 30, 'Post-operative follow-up', 'scheduled', 'routine'),
            
            # Oncology appointments
            (patient_ids[12], doctor_ids[6], appt_type_ids[1], base_date, '14:30:00', 45, 'Chemotherapy treatment session', 'completed', 'routine'),
            
            # Additional appointments
            (patient_ids[13], doctor_ids[0], appt_type_ids[0], base_date + timedelta(days=10), '10:00:00', 30, 'Routine ICU follow-up', 'scheduled', 'routine'),
            (patient_ids[14], doctor_ids[8], appt_type_ids[0], base_date + timedelta(days=5), '11:00:00', 45, 'Prenatal visit - OBG', 'completed', 'routine'),
        ]
        
        for i, (pat_id, doc_id, type_id, appt_date, appt_time, duration, reason, status, priority) in enumerate(appointment_data):
            if pat_id and doc_id:
                appt_num = f'APT{str(i+1).zfill(4)}'
                room = room_ids[i % len(room_ids)] if room_ids else None
                appointments.append((appt_num, pat_id, doc_id, type_id, appt_date, appt_time, duration, room, reason, status, priority))
        
        if appointments:
            sql = "INSERT IGNORE INTO appointments (appointment_number, patient_id, doctor_id, appointment_type_id, appointment_date, appointment_time, duration_minutes, room_id, reason, status, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, appointments)
            logger.info(f"Loaded {cursor.rowcount} appointment records")
        
        # 3. Load Appointment Cancellations (audit trail)
        cursor.execute("SELECT appointment_id FROM appointments WHERE status = 'scheduled' LIMIT 3")
        scheduled_appts = [row[0] for row in cursor.fetchall()]
        
        if scheduled_appts:
            cancellations = [
                (scheduled_appts[0], 'patient', datetime(2024, 3, 14, 15, 30), 'Patient unable to attend due to work conflict', False, None, 'Patient called to cancel same day'),
            ]
            
            if len(scheduled_appts) > 1:
                cancellations.append((scheduled_appts[1], 'system', datetime(2024, 3, 15, 9, 0), 'Doctor emergency - double booked',  True, None, 'System auto-canceled due to conflict'))
            
            sql = "INSERT IGNORE INTO appointment_cancellations (appointment_id, cancelled_by, cancellation_date, reason, reschedule_requested, new_appointment_id, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, cancellations)
            logger.info(f"Loaded {cursor.rowcount} appointment cancellation records")
    
    # 4. Load Encounters (patient visits/admissions)
    if patient_ids and doctor_ids and dept_ids:
        encounter_date = datetime(2024, 3, 15, 9, 30)
        encounters = []
        encounter_mapping = []  # Track encounters for later use
        
        # Create more diverse encounters including surgical
        for i in range(min(8, len(patient_ids))):
            enc_num = f'ENC{str(i+1).zfill(5)}'
            pat_id = patient_ids[i]
            doc_id = doctor_ids[i % len(doctor_ids)]
            dept_id = dept_ids[i % len(dept_ids)]
            room_id = room_ids[i % len(room_ids)] if room_ids else None
            
            # Make some encounters surgical type
            if i in [3, 5]:  # surgical encounters
                enc_type = 'surgical'
                bed_id = bed_ids[i % len(bed_ids)] if bed_ids else None
                admission_date = encounter_date + timedelta(days=i)
                discharge_date = admission_date + timedelta(days=2)
            else:
                enc_type = 'outpatient'
                bed_id = None
                admission_date = None
                discharge_date = None
            
            encounters.append((enc_num, pat_id, doc_id, None, 
                             encounter_date + timedelta(days=i), enc_type, dept_id, 
                             room_id, bed_id, f'Chief complaint {i}', None, 
                             admission_date, discharge_date, None, 'completed', None))
            encounter_mapping.append((i, pat_id, doc_id, encounter_date + timedelta(days=i), enc_type))
        
        if encounters:
            sql = "INSERT IGNORE INTO encounters (encounter_number, patient_id, doctor_id, appointment_id, encounter_date, encounter_type, department_id, room_id, bed_id, chief_complaint, present_illness, admission_date, discharge_date, length_of_stay, status, discharge_disposition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, encounters)
            logger.info(f"Loaded {cursor.rowcount} encounter records")
    
    # Get encounter IDs for subsequent records
    cursor.execute("SELECT encounter_id FROM encounters ORDER BY encounter_id")
    encounter_ids = [row[0] for row in cursor.fetchall()]
    
    # 5. Load Encounter Vitals
    if encounter_ids and nurse_ids:
        vitals = []
        
        for i, enc_id in enumerate(encounter_ids[:10]):
            # Multiple vitals per encounter
            base_time = datetime(2024, 3, 15, 10, 0) + timedelta(hours=i)
            
            vital_readings = [
                (enc_id, base_time, nurse_ids[i % len(nurse_ids)], 98.6, 120, 78, 72, 16, 98.5, 165.5, 70.0, 24.5, 5, 'Patient stable, alert and oriented'),
                (enc_id, base_time + timedelta(hours=4), nurse_ids[(i+1) % len(nurse_ids)], 98.8, 118, 76, 70, 15, 97.8, 165.5, 70.0, 24.5, 3, 'Patient doing well, pain controlled'),
            ]
            
            vitals.extend(vital_readings)
        
        if vitals:
            sql = "INSERT IGNORE INTO encounter_vitals (encounter_id, recorded_datetime, recorded_by, temperature, blood_pressure_systolic, blood_pressure_diastolic, heart_rate, respiratory_rate, oxygen_saturation, weight, height, bmi, pain_score, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, vitals)
            logger.info(f"Loaded {cursor.rowcount} encounter vital records")
    
    # 6. Load Encounter Diagnoses
    if encounter_ids and icd_ids:
        diagnoses = []
        
        diagnosis_mappings = [
            (0, 'Type 2 Diabetes', 'primary', 'moderate'),
            (0, 'Hypertension', 'primary', 'moderate'),
            (1, 'Essential Hypertension', 'primary', 'mild'),
            (2, 'Migraine without aura', 'primary', 'moderate'),
            (3, 'Generalized seizure disorder', 'primary', 'severe'),
            (4, 'Contusion of chest wall', 'primary', 'moderate'),
            (5, 'Acute abdomen NOS', 'primary', 'severe'),
            (6, 'Hernia', 'primary', 'moderate'),
            (7, 'Malignant neoplasm', 'primary', 'severe'),
        ]
        
        for idx, diagnosis_desc, diag_type, severity in diagnosis_mappings:
            if idx < len(encounter_ids) and icd_ids:
                diag_onset = datetime(2024, 1, 1).date() if idx < 4 else datetime(2024, 3, 15).date()
                diagnoses.append((encounter_ids[idx], icd_ids[idx % len(icd_ids)], diagnosis_desc, diag_type, severity, diag_onset, None, idx < 3, f'{diagnosis_desc} - confirmed diagnosis'))
        
        if diagnoses:
            sql = "INSERT IGNORE INTO encounter_diagnoses (encounter_id, icd_code_id, diagnosis_description, diagnosis_type, severity, onset_date, resolution_date, is_chronic, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, diagnoses)
            logger.info(f"Loaded {cursor.rowcount} encounter diagnosis records")
    
    # 7. Load Encounter Procedures
    if encounter_ids and cpt_ids and doctor_ids:
        procedures = []
        
        # Only add procedures to appropriate encounter types (surgical/inpatient)
        cursor.execute("SELECT encounter_id, encounter_type FROM encounters WHERE encounter_type IN ('surgical', 'inpatient')")
        surgical_encounters = [row for row in cursor.fetchall()]
        
        if surgical_encounters:
            for i, (enc_id, enc_type) in enumerate(surgical_encounters[:5]):
                proc_datetime = datetime(2024, 3, 15, 8, 0) + timedelta(days=i)
                procedures.append((enc_id, cpt_ids[i % len(cpt_ids)], f'Procedure {i+1}', f'Surgical procedure {i+1} description', doctor_ids[i % len(doctor_ids)], None, proc_datetime, 45, room_ids[0] if room_ids else None, 'local' if i % 2 == 0 else 'general', 'Procedure completed successfully', None, 'completed'))
        
        if procedures:
            sql = "INSERT IGNORE INTO encounter_procedures (encounter_id, cpt_code_id, procedure_name, procedure_description, performed_by, assisted_by, procedure_datetime, duration_minutes, room_id, anesthesia_type, outcome, complications, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, procedures)
            logger.info(f"Loaded {cursor.rowcount} encounter procedure records")
    
    # 8. Load Clinical Notes
    if encounter_ids and doctor_ids and nurse_ids:
        notes = []
        
        for i, enc_id in enumerate(encounter_ids[:15]):
            author = doctor_ids[i % len(doctor_ids)] if i % 2 == 0 else nurse_ids[i % len(nurse_ids)]
            author_type = 'doctor' if i % 2 == 0 else 'nurse'
            note_datetime = datetime(2024, 3, 15, 10, 0) + timedelta(hours=i)
            
            note_types = ['progress', 'admission', 'discharge', 'operative', 'consultation'] if i < 5 else ['progress', 'nursing']
            note_type = note_types[i % len(note_types)]
            
            note_text = f'Patient {i+1} - {note_type.upper()} NOTE\n'
            if note_type == 'progress':
                note_text += 'Patient presenting with documented chief complaint. Vital signs stable. Physical examination performed.'
            elif note_type == 'admission':
                note_text += 'Patient admitted to facility. Complete history and physical performed. Initial diagnostic workup initiated.'
            elif note_type == 'discharge':
                note_text += 'Patient discharged in stable condition. Follow-up appointments scheduled. Prescriptions provided.'
            elif note_type == 'operative':
                note_text += 'Surgical procedure performed successfully. No intraoperative complications. Patient tolerated procedure well.'
            else:
                note_text += 'Nursing assessment completed. Patient comfortable, pain managed. Care plan updated.'
            
            notes.append((enc_id, note_type, author, author_type, note_datetime, f'{note_type.title()} Note', note_text, True, note_datetime, False, None))
        
        if notes:
            sql = "INSERT IGNORE INTO clinical_notes (encounter_id, note_type, author_id, author_type, note_datetime, subject, note_text, is_signed, signed_datetime, is_amended, amendment_note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, notes)
            logger.info(f"Loaded {cursor.rowcount} clinical note records")
    
    # 9. Load Bed Assignments (for inpatient encounters)
    if patient_ids and bed_ids and encounter_ids:
        bed_assignments = []
        
        cursor.execute("SELECT encounter_id FROM encounters WHERE encounter_type IN ('inpatient', 'surgical') LIMIT 5")
        inpatient_encounters = [row[0] for row in cursor.fetchall()]
        
        for i, enc_id in enumerate(inpatient_encounters):
            cursor.execute(f"SELECT patient_id FROM encounters WHERE encounter_id = {enc_id}")
            result = cursor.fetchone()
            if result:
                pat_id = result[0]
                assign_datetime = datetime(2024, 3, 15, 8, 0) + timedelta(days=i)
                discharge_datetime = (assign_datetime + timedelta(days=2 + i % 3)).replace(hour=14, minute=0)
                
                bed_assignments.append((pat_id, bed_ids[i % len(bed_ids)], enc_id, assign_datetime, discharge_datetime, 'Admitted for care', nurse_ids[i % len(nurse_ids)] if nurse_ids else None, 'discharged'))
        
        if bed_assignments:
            sql = "INSERT IGNORE INTO bed_assignments (patient_id, bed_id, encounter_id, assignment_datetime, discharge_datetime, reason, assigned_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, bed_assignments)
            logger.info(f"Loaded {cursor.rowcount} bed assignment records")
    
    # Insurance Policies (legacy support)
    cursor.execute("SELECT COUNT(*) FROM patient_insurance_policies")
    if cursor.fetchone()[0] == 0 and patient_ids:
        cursor.execute("SELECT insurance_company_id FROM insurance_companies LIMIT 5")
        insurance_ids = [row[0] for row in cursor.fetchall()]
        
        if insurance_ids:
            cursor.execute("SELECT plan_id FROM insurance_plans LIMIT 3")
            plan_ids = [row[0] for row in cursor.fetchall()]
            
            if not plan_ids and len(insurance_ids) >= 2:
                plans = [
                    (insurance_ids[0], 'BCBS Premium PPO', 'PPO-PREM', 'PPO', 'family', 2000.00, 25.00, True),
                    (insurance_ids[1], 'UHC Choice Plus', 'CHOICE-PLUS', 'PPO', 'family', 2500.00, 30.00, True),
                ]
                
                sql = "INSERT IGNORE INTO insurance_plans (insurance_company_id, plan_name, plan_code, plan_type, coverage_level, deductible_amount, copay_amount, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, plans)
                logger.info(f"Loaded {cursor.rowcount} insurance plan records")
                
                cursor.execute("SELECT plan_id FROM insurance_plans LIMIT 3")
                plan_ids = [row[0] for row in cursor.fetchall()]
            
            if plan_ids:
                patient_names = [('Alice', 'Anderson'), ('Robert', 'Taylor'), ('Jennifer', 'Martinez'), ('William', 'Garcia'), ('Lisa', 'Rodriguez')]
                policies = [
                    (patient_ids[i], plan_ids[i % len(plan_ids)], f'POL{str(i).zfill(5)}', 'GRP001', f'{patient_names[i % len(patient_names)][0]} {patient_names[i % len(patient_names)][1]}', 'self', '2023-01-01', True, 'active')
                    for i in range(min(len(patient_ids), 5))
                ]
                
                sql = "INSERT IGNORE INTO patient_insurance_policies (patient_id, insurance_plan_id, policy_number, group_number, subscriber_name, subscriber_relationship, policy_start_date, is_primary, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, policies)
                logger.info(f"Loaded {cursor.rowcount} insurance policy records")
    
    print("   [OK] Transactional data loaded successfully")
    return True


def load_laboratory_data(cursor):
    """Load laboratory and diagnostics data (lab orders, tests, results)"""
    print("\n[6/11] Loading Laboratory Data (lab orders, tests, results)...")
    
    # Get needed IDs
    cursor.execute("SELECT encounter_id FROM encounters LIMIT 10")
    encounter_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT patient_id FROM patients LIMIT 10")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT doctor_id FROM doctors LIMIT 10")
    doctor_ids = [row[0] for row in cursor.fetchall()]
    
    if encounter_ids and patient_ids and doctor_ids:
        # Load Lab Orders
        lab_orders = []
        for i in range(min(10, len(encounter_ids))):
            order_num = f'LAB{str(i+1).zfill(5)}'
            lab_orders.append((order_num, encounter_ids[i], patient_ids[i % len(patient_ids)], doctor_ids[i % len(doctor_ids)], 
                             datetime(2024, 3, 15, 10, 0) + timedelta(hours=i), 'routine', 'ordered', None, 'Routine lab panel'))
        
        sql = "INSERT IGNORE INTO lab_orders (order_number, encounter_id, patient_id, ordering_doctor_id, order_datetime, priority, status, collection_datetime, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, lab_orders)
        logger.info(f"Loaded {cursor.rowcount} lab order records")
        
        # Get lab order IDs for tests
        cursor.execute("SELECT order_id FROM lab_orders LIMIT 10")
        order_ids = [row[0] for row in cursor.fetchall()]
        
        # Load Lab Tests
        if order_ids:
            test_configs = [
                ('CBC', 'Complete Blood Count', 'Hematology', 'Whole Blood'),
                ('CMP', 'Comprehensive Metabolic Panel', 'Chemistry', 'Serum'),
                ('TSH', 'Thyroid Stimulating Hormone', 'Endocrinology', 'Serum'),
                ('BUN', 'Blood Urea Nitrogen', 'Chemistry', 'Serum'),
                ('CREAT', 'Creatinine', 'Chemistry', 'Serum'),
                ('GLUC', 'Glucose', 'Chemistry', 'Serum'),
            ]
            
            lab_tests = []
            for idx, order_id in enumerate(order_ids[:5]):
                test_idx = idx % len(test_configs)
                code, name, category, specimen = test_configs[test_idx]
                lab_tests.append((order_id, code, name, category, specimen, 'completed'))
            
            sql = "INSERT IGNORE INTO lab_tests (order_id, test_code, test_name, test_category, specimen_type, status) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, lab_tests)
            logger.info(f"Loaded {cursor.rowcount} lab test records")
            
            # Get lab test IDs for results
            cursor.execute("SELECT test_id FROM lab_tests LIMIT 10")
            test_ids = [row[0] for row in cursor.fetchall()]
            
            # Load Lab Results
            if test_ids:
                lab_results = []
                result_data = [
                    ('7.2', 'g/dL', '7.0-7.5', 'normal'),
                    ('95', 'mg/dL', '70-100', 'normal'),
                    ('2.5', 'mIU/L', '0.4-4.0', 'normal'),
                    ('15', 'mg/dL', '7-20', 'normal'),
                    ('0.8', 'mg/dL', '0.6-1.2', 'normal'),
                    ('92', 'mg/dL', '70-100', 'normal'),
                ]
                
                for idx, test_id in enumerate(test_ids[:5]):
                    value, unit, range_val, flag = result_data[idx % len(result_data)]
                    lab_results.append((test_id, value, unit, range_val, flag, datetime(2024, 3, 15, 14, 0), 'Lab Tech', doctor_ids[idx % len(doctor_ids)], datetime(2024, 3, 15, 14, 30), 'Normal results'))
                
                sql = "INSERT IGNORE INTO lab_results (test_id, result_value, result_unit, reference_range, abnormal_flag, result_datetime, performed_by, verified_by, verification_datetime, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, lab_results)
                logger.info(f"Loaded {cursor.rowcount} lab result records")
    
    print("   [OK] Laboratory data loaded successfully")
    return True


def load_radiology_data(cursor):
    """Load radiology and imaging data (orders, results)"""
    print("\n[7/11] Loading Radiology Data (imaging orders, results)...")
    
    # Get needed IDs
    cursor.execute("SELECT encounter_id FROM encounters LIMIT 10")
    encounter_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT patient_id FROM patients LIMIT 10")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT doctor_id FROM doctors LIMIT 10")
    doctor_ids = [row[0] for row in cursor.fetchall()]
    
    if encounter_ids and patient_ids and doctor_ids:
        # Load Radiology Orders
        radiology_orders = []
        modalities = [('X-Ray', 'Chest'), ('CT', 'Head'), ('MRI', 'Spine'), ('Ultrasound', 'Abdomen'), ('CT', 'Thorax')]
        
        for i in range(min(8, len(encounter_ids))):
            modality, body_part = modalities[i % len(modalities)]
            order_num = f'RAD{str(i+1).zfill(5)}'
            radiology_orders.append((order_num, encounter_ids[i], patient_ids[i % len(patient_ids)], doctor_ids[i % len(doctor_ids)], 
                                    f'{body_part} {modality}', body_part, modality, 
                                    datetime(2024, 3, 15, 9, 0) + timedelta(hours=i), 
                                    (datetime(2024, 3, 15, 9, 0) + timedelta(hours=i+1)).time(), 
                                    'routine', f'{body_part} evaluation', i % 2 == 0, 'ordered', 'Routine imaging'))
        
        sql = "INSERT IGNORE INTO radiology_orders (order_number, encounter_id, patient_id, ordering_doctor_id, exam_type, body_part, modality, order_datetime, scheduled_datetime, priority, clinical_indication, contrast_used, status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, radiology_orders)
        logger.info(f"Loaded {cursor.rowcount} radiology order records")
        
        # Get radiology order IDs for results
        cursor.execute("SELECT order_id FROM radiology_orders LIMIT 10")
        rad_order_ids = [row[0] for row in cursor.fetchall()]
        
        # Load Radiology Results
        if rad_order_ids:
            rad_results = []
            for i, order_id in enumerate(rad_order_ids[:6]):
                rad_results.append((order_id, datetime(2024, 3, 15, 14, 0), doctor_ids[i % len(doctor_ids)],
                                  'No acute findings. Normal anatomical variants noted.',
                                  'Negative for acute pathology. Comparison to prior studies recommended.',
                                  'Complete radiology report text here.',
                                  False, datetime(2024, 3, 15, 15, 0), 'PACS_REF_001', 'final'))
            
            sql = "INSERT IGNORE INTO radiology_results (order_id, exam_datetime, radiologist_id, findings, impression, report_text, critical_findings, report_datetime, image_location, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, rad_results)
            logger.info(f"Loaded {cursor.rowcount} radiology result records")
    
    print("   [OK] Radiology data loaded successfully")
    return True


def load_pharmacy_data(cursor):
    """Load pharmacy and medication data"""
    print("\n[8/11] Loading Pharmacy Data (medications, prescriptions, inventory)...")
    
    # Get needed IDs
    cursor.execute("SELECT patient_id FROM patients LIMIT 10")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT doctor_id FROM doctors LIMIT 10")
    doctor_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT encounter_id FROM encounters LIMIT 10")
    encounter_ids = [row[0] for row in cursor.fetchall()]
    
    if patient_ids and doctor_ids and encounter_ids:
        # Get or create medications
        cursor.execute("SELECT medication_id FROM medications LIMIT 10")
        medication_ids = [row[0] for row in cursor.fetchall()]
        
        if not medication_ids:
            # Load common medications
            medications = [
                ('Aspirin', 'Aspirin', 'Bayer', 'Analgesic', '50580-001', 'tablet', '325mg', 'EA', 'Bayer', False, None, True, 0.50, 'active'),
                ('Ibuprofen', 'Ibuprofen', 'Advil', 'NSAID', '50458-008', 'tablet', '200mg', 'EA', 'Wyeth', False, None, True, 0.75, 'active'),
                ('Lisinopril', 'Lisinopril', 'Prinivil', 'ACE Inhibitor', '0093-0862', 'tablet', '10mg', 'EA', 'Merck', False, None, True, 2.50, 'active'),
                ('Metformin', 'Metformin', 'Glucophage', 'Antidiabetic', '0378-1803', 'tablet', '500mg', 'EA', 'Bristol-Myers', False, None, True, 1.00, 'active'),
                ('Amlodipine', 'Amlodipine', 'Norvasc', 'Calcium Channel Blocker', '0026-1887', 'tablet', '5mg', 'EA', 'Pfizer', False, None, True, 3.00, 'active'),
                ('Omeprazole', 'Omeprazole', 'Prilosec', 'Proton Pump Inhibitor', '0007-4305', 'capsule', '20mg', 'EA', 'Astrazeneca', False, None, True, 2.00, 'active'),
                ('Sertraline', 'Sertraline', 'Zoloft', 'SSRI', '0049-3980', 'tablet', '50mg', 'EA', 'Pfizer', False, None, True, 1.50, 'active'),
                ('Amoxicillin', 'Amoxicillin', 'Amoxil', 'Antibiotic', '0615-6840', 'capsule', '500mg', 'EA', 'Glaxo', False, None, True, 0.80, 'active'),
            ]
            
            sql = "INSERT IGNORE INTO medications (medication_name, generic_name, brand_name, drug_class, ndc_code, dosage_form, strength, unit_of_measure, manufacturer, is_controlled, dea_schedule, requires_prescription, unit_price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, medications)
            logger.info(f"Loaded {cursor.rowcount} medication records")
            
            cursor.execute("SELECT medication_id FROM medications LIMIT 10")
            medication_ids = [row[0] for row in cursor.fetchall()]
        
        # Load Drug Interactions
        if len(medication_ids) >= 2:
            interactions = [
                (medication_ids[0], medication_ids[1], 'minor', 'May increase GI side effects', 'Monitor for GI upset', 'Take with food'),
                (medication_ids[2], medication_ids[3], 'moderate', 'Increased hypoglycemia risk', 'Monitor blood glucose', 'Check glucose regularly'),
            ]
            
            sql = "INSERT IGNORE INTO drug_interactions (medication_id_1, medication_id_2, interaction_type, description, clinical_effect, recommendation) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, interactions)
            logger.info(f"Loaded {cursor.rowcount} drug interaction records")
        
        # Load Prescriptions
        if medication_ids:
            prescriptions = []
            for i in range(min(12, len(patient_ids), len(encounter_ids))):
                rx_num = f'RX{str(i+1).zfill(6)}'
                prescriptions.append((rx_num, encounter_ids[i], patient_ids[i], doctor_ids[i % len(doctor_ids)], 
                                    medication_ids[i % len(medication_ids)], '1 tablet', 'tablet', 'oral', 'twice daily', '30 days',
                                    30, 30, 2, 2, datetime(2024, 3, 15).date(), datetime(2024, 3, 15).date(), 
                                    (datetime(2024, 3, 15) + timedelta(days=30)).date(), 'Take with food', 'Hypertension management',
                                    None, 'Dr. John', 'active', None, None, False))
            
            sql = "INSERT IGNORE INTO prescriptions (prescription_number, encounter_id, patient_id, doctor_id, medication_id, dosage, dosage_unit, route, frequency, duration, quantity_prescribed, quantity_dispensed, refills_allowed, refills_remaining, prescription_date, start_date, end_date, instructions, indication, pharmacy_notes, prescriber_signature, status, discontinuation_reason, original_prescription_id, is_refill) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, prescriptions)
            logger.info(f"Loaded {cursor.rowcount} prescription records")
            
            # Get prescription IDs for refills
            cursor.execute("SELECT prescription_id FROM prescriptions LIMIT 5")
            rx_ids = [row[0] for row in cursor.fetchall()]
            
            # Load Prescription Refills
            if rx_ids:
                refills = [
                    (rx_ids[0], 1, datetime(2024, 3, 20).date(), 30, 'Pharmacist', 'CVS Pharmacy', '555-1234', 15.00, 'First refill'),
                ] if len(rx_ids) > 0 else []
                
                if refills:
                    sql = "INSERT IGNORE INTO prescription_refills (prescription_id, refill_number, refill_date, quantity_dispensed, dispensed_by, pharmacy_name, pharmacy_phone, cost, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, refills)
                    logger.info(f"Loaded {cursor.rowcount} prescription refill records")
            
            # Load Medication Inventory
            inventory_records = []
            for med_id in medication_ids[:8]:
                inventory_records.append((med_id, 'LOT001', (datetime(2024, 12, 31)).date(), 500, 100, 'Pharmacy Shelf A', datetime(2024, 3, 1).date(), 1000, 'available'))
            
            sql = "INSERT IGNORE INTO medication_inventory (medication_id, lot_number, expiration_date, quantity_on_hand, reorder_level, location, last_restock_date, last_restock_quantity, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, inventory_records)
            logger.info(f"Loaded {cursor.rowcount} medication inventory records")
            
            # Load Pharmacy Orders
            pharmacy_orders_list = []
            for i, med_id in enumerate(medication_ids[:5]):
                po_num = f'PO{str(i+1).zfill(5)}'
                pharmacy_orders_list.append((po_num, med_id, 'Cardinal Health', datetime(2024, 3, 1).date(), 
                                           (datetime(2024, 3, 5)).date(), (datetime(2024, 3, 5)).date(),
                                           1000, 1000, 0.50, 500.00, 'received', None, None, 'Monthly order', datetime(2024, 3, 5).date()))
            
            sql = "INSERT IGNORE INTO pharmacy_orders (order_number, medication_id, supplier_name, order_date, expected_delivery_date, actual_delivery_date, quantity_ordered, quantity_received, unit_cost, total_cost, order_status, ordered_by, received_by, notes, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, pharmacy_orders_list)
            logger.info(f"Loaded {cursor.rowcount} pharmacy order records")
    
    print("   [OK] Pharmacy data loaded successfully")
    return True


def load_insurance_extended_data(cursor):
    """Load extended insurance data (authorizations, claims, claim items)"""
    print("\n[9/11] Loading Insurance Data (authorizations, claims)...")
    
    # Get needed IDs
    cursor.execute("SELECT patient_id FROM patients LIMIT 10")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT policy_id FROM patient_insurance_policies LIMIT 10")
    policy_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT encounter_id FROM encounters LIMIT 10")
    encounter_ids = [row[0] for row in cursor.fetchall()]
    
    if patient_ids and policy_ids:
        # Load Insurance Authorizations
        authorizations = []
        for i in range(min(6, len(patient_ids), len(policy_ids))):
            auth_num = f'AUTH{str(i+1).zfill(6)}'
            authorizations.append((patient_ids[i], policy_ids[i % len(policy_ids)], auth_num, 'Hospitalization',
                                 None, 5, 0,
                                 datetime(2024, 3, 10).date(), datetime(2024, 3, 10).date(), datetime(2024, 4, 10).date(),
                                 'approved', 'Pre-authorization for surgery'))
        
        sql = "INSERT IGNORE INTO insurance_authorizations (patient_id, policy_id, authorization_number, service_type, cpt_code_id, units_authorized, units_used, authorization_date, effective_date, expiration_date, status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, authorizations)
        logger.info(f"Loaded {cursor.rowcount} insurance authorization records")
        
        # Load Insurance Claims
        if encounter_ids:
            claims = []
            for i in range(min(8, len(encounter_ids))):
                claim_num = f'CLAIM{str(i+1).zfill(6)}'
                claims.append((claim_num, patient_ids[i % len(patient_ids)], policy_ids[i % len(policy_ids)],
                             encounter_ids[i], datetime(2024, 3, 15).date(), 
                             datetime(2024, 3, 15).date(), datetime(2024, 3, 15).date(),
                             1500.00, 1200.00, 1000.00, 200.00, 0.00,
                             datetime(2024, 3, 16).date(), datetime(2024, 3, 20).date(), datetime(2024, 3, 25).date(),
                             'paid', None, 'Inpatient hospitalization claim'))
                
            sql = "INSERT IGNORE INTO insurance_claims (claim_number, patient_id, policy_id, encounter_id, claim_date, service_date_from, service_date_to, total_charge, allowed_amount, paid_amount, patient_responsibility, adjustment_amount, submission_date, adjudication_date, payment_date, status, denial_reason, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, claims)
            logger.info(f"Loaded {cursor.rowcount} insurance claim records")
            
            # Get claim IDs for claim items
            cursor.execute("SELECT claim_id FROM insurance_claims LIMIT 5")
            claim_ids = [row[0] for row in cursor.fetchall()]
            
            # Load Insurance Claim Items
            if claim_ids:
                claim_items = []
                for i, claim_id in enumerate(claim_ids[:4]):
                    claim_items.append((claim_id, i+1, datetime(2024, 3, 15).date(),
                                      'Hospital service', 1, 500.00, 500.00, 400.00, 400.00, 0.00,
                                      None))
                
                sql = "INSERT IGNORE INTO insurance_claim_items (claim_id, line_number, service_date, service_description, quantity, unit_charge, total_charge, allowed_amount, paid_amount, adjustment_amount, adjustment_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, claim_items)
                logger.info(f"Loaded {cursor.rowcount} insurance claim item records")
    
    print("   [OK] Insurance data loaded successfully")
    return True


def load_billing_data(cursor):
    """Load billing and payment data"""
    print("\n[10/11] Loading Billing Data (invoices, payments)...")
    
    # Get needed IDs
    cursor.execute("SELECT patient_id FROM patients LIMIT 10")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT encounter_id FROM encounters LIMIT 10")
    encounter_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT cpt_id FROM cpt_codes LIMIT 5")
    cpt_ids = [row[0] for row in cursor.fetchall()]
    
    if patient_ids and encounter_ids:
        # Load Invoices
        invoices = []
        for i in range(min(10, len(patient_ids))):
            inv_num = f'INV{str(i+1).zfill(6)}'
            subtotal = 1000.00 + (i * 100)
            invoices.append((inv_num, patient_ids[i], encounter_ids[i % len(encounter_ids)],
                           datetime(2024, 3, 15).date(), (datetime(2024, 4, 15)).date(),
                           subtotal, 50.00, 100.00, subtotal + 50 - 100, 500.00, 'partial', 'Net 30', 'Regular invoice'))
            
            sql = "INSERT IGNORE INTO invoices (invoice_number, patient_id, encounter_id, invoice_date, due_date, subtotal_amount, tax_amount, discount_amount, total_amount, amount_paid, payment_status, payment_terms, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, invoices)
            logger.info(f"Loaded {cursor.rowcount} invoice records")
        
        # Get invoice IDs for items
        cursor.execute("SELECT invoice_id FROM invoices LIMIT 10")
        invoice_ids = [row[0] for row in cursor.fetchall()]
        
        # Load Invoice Items
        if invoice_ids and cpt_ids:
            invoice_items = []
            for inv_id in invoice_ids[:8]:
                for j in range(2):  # 2 items per invoice
                    invoice_items.append((inv_id, j+1, 'service', cpt_ids[j % len(cpt_ids)],
                                        f'Service item {j+1}', 1, 500.00, 500.00, 0.00, 25.00))
            
            sql = "INSERT IGNORE INTO invoice_items (invoice_id, line_number, item_type, cpt_code_id, description, quantity, unit_price, total_price, discount_amount, tax_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, invoice_items)
            logger.info(f"Loaded {cursor.rowcount} invoice item records")
        
        # Load Payment Transactions
        payment_transactions = []
        for i in range(min(6, len(invoice_ids))):
            txn_num = f'TXN{str(i+1).zfill(6)}'
            payment_transactions.append((txn_num, invoice_ids[i], patient_ids[i % len(patient_ids)],
                                       (datetime(2024, 3, 20) + timedelta(days=i)).date(), 500.00, 'check',
                                       f'Check #{1001+i}', None, None, None, 'Received payment', 'completed'))
            
            sql = "INSERT IGNORE INTO payment_transactions (transaction_number, invoice_id, patient_id, payment_date, payment_amount, payment_method, payment_reference, card_type, card_last_four, processed_by, notes, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, payment_transactions)
            logger.info(f"Loaded {cursor.rowcount} payment transaction records")
    
    print("   [OK] Billing data loaded successfully")
    return True


def load_admin_data(cursor):
    """Load system administration data (users, roles, audit logs)"""
    print("\n[11/11] Loading Admin Data (users, roles, audit logs)...")
    
    # Load Roles first
    roles = [
        ('admin', 'System administrator with full access', '["read", "write", "delete", "admin"]'),
        ('doctor', 'Physician with patient care access', '["read", "write", "patient_care"]'),
        ('nurse', 'Nursing staff with limited access', '["read", "write", "patient_care"]'),
        ('staff', 'Administrative staff with view access', '["read"]'),
        ('receptionist', 'Receptionist with appointment access', '["read", "write", "appointments"]'),
    ]
    
    sql = "INSERT IGNORE INTO roles (role_name, description, permissions) VALUES (%s, %s, %s)"
    cursor.executemany(sql, roles)
    logger.info(f"Loaded {cursor.rowcount} role records")
    
    # Get role IDs
    cursor.execute("SELECT role_name, role_id FROM roles")
    role_ids_dict = {}
    for role_name, role_id in cursor.fetchall():
        role_ids_dict[role_name] = role_id
    
    # Load Users
    users = [
        ('admin_user', 'password_hash_here', 'admin@hospital.com', 'admin', None, True, datetime(2024, 3, 1, 8, 0), None, 0, False),
        ('dr_smith', 'password_hash_here', 'john.smith@hospital.com', 'doctor', 1, True, datetime(2024, 3, 15, 9, 0), None, 0, False),
        ('dr_johnson', 'password_hash_here', 'sarah.johnson@hospital.com', 'doctor', 2, True, None, None, 0, False),
        ('nurse_anderson', 'password_hash_here', 'lisa.anderson@hospital.com', 'nurse', 3, True, datetime(2024, 3, 15, 7, 0), None, 0, False),
        ('staff_williams', 'password_hash_here', 'james.williams@hospital.com', 'staff', None, True, datetime(2024, 3, 10, 8, 0), None, 0, False),
    ]
    
    sql = "INSERT IGNORE INTO users (username, password_hash, email, user_type, reference_id, is_active, last_login, password_changed_at, failed_login_attempts, account_locked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, users)
    logger.info(f"Loaded {cursor.rowcount} user records")
    
    # Get user IDs for user-role assignments
    cursor.execute("SELECT user_id FROM users LIMIT 5")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    # Load User Roles
    if user_ids and role_ids_dict:
        user_roles = [
            (user_ids[0], role_ids_dict.get('admin', 1), datetime(2024, 1, 1).date(), None),
            (user_ids[1], role_ids_dict.get('doctor', 2), datetime(2024, 1, 1).date(), None),
            (user_ids[2], role_ids_dict.get('doctor', 2), datetime(2024, 1, 1).date(), None),
            (user_ids[3], role_ids_dict.get('nurse', 3), datetime(2024, 1, 1).date(), None),
            (user_ids[4], role_ids_dict.get('staff', 4), datetime(2024, 1, 1).date(), None),
        ]
        
        sql = "INSERT IGNORE INTO user_roles (user_id, role_id, assigned_date, assigned_by) VALUES (%s, %s, %s, %s)"
        cursor.executemany(sql, user_roles)
        logger.info(f"Loaded {cursor.rowcount} user role records")
    
    # Load Audit Logs
    audit_logs = [
        ('patients', 1, 'INSERT', user_ids[0] if user_ids else 1, 'admin', None, '{"patient_id": 1, "name": "Alice Anderson"}', '192.168.1.100', 'Mozilla/5.0', datetime(2024, 3, 1, 10, 0)),
        ('medications', 1, 'INSERT', user_ids[0] if user_ids else 1, 'admin', None, '{"medication_id": 1, "name": "Aspirin"}', '192.168.1.100', 'Mozilla/5.0', datetime(2024, 3, 2, 10, 0)),
        ('prescriptions', 1, 'INSERT', user_ids[1] if len(user_ids) > 1 else 1, 'doctor', None, '{"prescription_id": 1}', '192.168.1.101', 'Mozilla/5.0', datetime(2024, 3, 15, 10, 0)),
    ]
    
    sql = "INSERT IGNORE INTO audit_logs (table_name, record_id, action, user_id, user_type, old_values, new_values, ip_address, user_agent, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, audit_logs)
    logger.info(f"Loaded {cursor.rowcount} audit log records")
    
    print("   [OK] Admin data loaded successfully")
    return True


def load_all_fake_data():
    """Main function to load all fake data in proper order"""
    connection = None
    
    try:
        log_path = setup_fake_data_log()
        logger.info(f"Fake data log file: {log_path}")

        # Connect to database
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            logger.info("Connected to hospital_OLTP_system database")
            
            print("\n" + "=" * 60)
            print("HOSPITAL OLTP SYSTEM - FAKE DATA LOADER")
            print("=" * 60)
            
            # Load data in dependency order - use fresh cursor for each layer
            success = True
            
            cursor = connection.cursor()
            success = load_reference_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_organizational_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_staff_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_patient_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_transactional_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_laboratory_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_radiology_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_pharmacy_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_insurance_extended_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_billing_data(cursor) and success
            cursor.close()
            connection.commit()
            
            cursor = connection.cursor()
            success = load_admin_data(cursor) and success
            cursor.close()
            connection.commit()
            
            print("\n" + "=" * 60)
            print("[OK] ALL FAKE DATA LOADED SUCCESSFULLY")
            print("=" * 60)
            print("\nData loaded with PK-FK relationships intact")
            print("Hospital OLTP system is ready for testing\n")
            
            return success
            
    except Error as e:
        logger.error(f"Error loading fake data: {e}")
        print(f"\n[FAILED] Error: {e}")
        if connection and connection.is_connected():
            connection.rollback()
        return False
    
    finally:
        try:
            if connection and connection.is_connected():
                connection.close()
        except:
            pass


if __name__ == "__main__":
    success = load_all_fake_data()
    sys.exit(0 if success else 1)
