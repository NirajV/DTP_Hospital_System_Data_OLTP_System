# Hospital OLTP System - Database Schema Documentation

## Overview
This database schema contains approximately **50 tables** organized into logical domains to support comprehensive hospital operations. The schema uses MySQL/MariaDB and implements comprehensive referential integrity through primary/foreign key relationships.

## Table Count Summary
- **Total Tables**: 50
- **Reference Tables**: 2 (ICD Codes, CPT Codes)
- **Organizational**: 6 (Departments, Facilities, Rooms, Beds, Equipment, Department Equipment)
- **Patient Domain**: 4 (Patients, Addresses, Emergency Contacts, Allergies)
- **Staff Domain**: 8 (Doctors, Nurses, Staff, Specialists, Schedules, Shifts, Assignments)
- **Appointments**: 3 (Appointment Types, Appointments, Cancellations)
- **Encounters**: 6 (Encounters, Vitals, Diagnoses, Procedures, Notes, Bed Assignments)
- **Laboratory**: 4 (Lab Orders, Lab Tests, Lab Results, Radiology Orders, Radiology Results)
- **Pharmacy**: 6 (Medications, Interactions, Prescriptions, Refills, Inventory, Orders)
- **Insurance**: 7 (Companies, Plans, Policies, Authorizations, Claims, Claim Items, Invoices)
- **Billing**: 3 (Invoices, Invoice Items, Payment Transactions)
- **System**: 4 (Users, Roles, User Roles, Audit Logs)

## Domain Architecture

### 1. Reference & Lookup Tables (2 tables)

#### icd_codes
International Classification of Diseases codes for diagnoses
- **Primary Key**: icd_id
- **Unique**: code
- **Indexes**: code, category
- **Purpose**: Standard diagnosis coding

#### cpt_codes
Current Procedural Terminology codes for procedures
- **Primary Key**: cpt_id
- **Unique**: code
- **Indexes**: code, category
- **Purpose**: Standard procedure/service coding

---

### 2. Organizational Structure (6 tables)

#### departments
Hospital departments and administrative units
- **Primary Key**: department_id
- **Unique**: department_name, department_code
- **Key Fields**: manager_id, budget, status
- **Relationships**: Referenced by doctors, nurses, staff, rooms

#### facilities
Physical buildings and structures
- **Primary Key**: facility_id
- **Key Fields**: facility_type (building/wing/floor/unit)
- **Relationships**: Parent to rooms

#### rooms
Individual rooms within facilities
- **Primary Key**: room_id
- **Foreign Keys**: facility_id → facilities, department_id → departments
- **Key Fields**: room_number, room_type, capacity, status
- **Relationships**: Parent to beds, referenced by appointments, encounters

#### beds
Individual beds within rooms
- **Primary Key**: bed_id
- **Foreign Keys**: room_id → rooms
- **Key Fields**: bed_number, bed_type, is_occupied, status
- **Unique**: (room_id, bed_number)
- **Relationships**: Referenced by bed_assignments, encounters

#### equipment
Medical equipment inventory
- **Primary Key**: equipment_id
- **Unique**: serial_number
- **Key Fields**: equipment_type, manufacturer, status
- **Relationships**: Referenced by department_equipment

#### department_equipment
Equipment assignments to departments
- **Primary Key**: assignment_id
- **Foreign Keys**: department_id → departments, equipment_id → equipment
- **Purpose**: Track equipment location and usage

---

### 3. Patient Information (4 tables)

#### patients
Core patient demographics and registration
- **Primary Key**: patient_id
- **Unique**: mrn (Medical Record Number), ssn
- **Key Fields**: name, date_of_birth, gender, blood_group
- **Indexes**: mrn, name, dob, status
- **Relationships**: Parent to all patient-related tables

#### patient_addresses
Multiple addresses per patient
- **Primary Key**: address_id
- **Foreign Keys**: patient_id → patients
- **Key Fields**: address_type, is_primary
- **Purpose**: Support multiple address types

#### patient_emergency_contacts
Emergency contact information
- **Primary Key**: contact_id
- **Foreign Keys**: patient_id → patients
- **Key Fields**: contact_name, relationship, priority_order

#### patient_allergies
Patient allergy tracking
- **Primary Key**: allergy_id
- **Foreign Keys**: patient_id → patients
- **Key Fields**: allergen_type, severity, status
- **Indexes**: patient_id, allergen_type, status

---

### 4. Healthcare Providers (8 tables)

#### doctors
Medical staff with credentials
- **Primary Key**: doctor_id
- **Unique**: employee_id, email, license_number, npi_number
- **Foreign Keys**: department_id → departments
- **Key Fields**: specialization, license_number, npi_number
- **Indexes**: department_id, specialization, status, npi_number
- **Relationships**: Referenced by appointments, encounters, prescriptions

#### nurses
Nursing staff
- **Primary Key**: nurse_id
- **Unique**: employee_id, license_number, email
- **Foreign Keys**: department_id → departments
- **Key Fields**: license_type (RN/LPN/NP/CNS), shift_preference

#### staff
Administrative and support staff
- **Primary Key**: staff_id
- **Unique**: employee_id, email
- **Foreign Keys**: department_id → departments
- **Key Fields**: position, salary

#### specialists
Consulting specialists
- **Primary Key**: specialist_id
- **Foreign Keys**: doctor_id → doctors
- **Purpose**: Track specialist consultations

#### nurse_assignments
Patient-nurse assignments
- **Primary Key**: assignment_id
- **Foreign Keys**: nurse_id → nurses, patient_id → patients, bed_id → beds
- **Key Fields**: shift, assigned_date, end_date

#### staff_shifts
Shift scheduling
- **Primary Key**: shift_id
- **Foreign Keys**: staff_id → staff, nurse_id → nurses
- **Key Fields**: shift_date, shift_type, start_time, end_time

#### doctor_schedules
Weekly doctor availability
- **Primary Key**: schedule_id
- **Foreign Keys**: doctor_id → doctors, room_id → rooms
- **Key Fields**: day_of_week, start_time, end_time, max_patients

---

### 5. Appointments & Scheduling (3 tables)

#### appointment_types
Categorized appointment types
- **Primary Key**: type_id
- **Unique**: type_name
- **Key Fields**: default_duration, requires_preparation

#### appointments
Comprehensive appointment scheduling
- **Primary Key**: appointment_id
- **Unique**: appointment_number
- **Foreign Keys**: patient_id → patients, doctor_id → doctors, appointment_type_id → appointment_types, room_id → rooms
- **Key Fields**: appointment_date, appointment_time, status, priority
- **Indexes**: date, patient_id, doctor_id, status, type_id
- **Self-Reference**: parent_appointment_id for follow-ups

#### appointment_cancellations
Cancellation audit trail
- **Primary Key**: cancellation_id
- **Foreign Keys**: appointment_id → appointments, new_appointment_id → appointments
- **Purpose**: Track cancellation history and rescheduling

---

### 6. Clinical Encounters (6 tables)

#### encounters
Patient visits and admissions
- **Primary Key**: encounter_id
- **Unique**: encounter_number
- **Foreign Keys**: patient_id → patients, doctor_id → doctors, appointment_id → appointments, department_id → departments, room_id → rooms, bed_id → beds
- **Key Fields**: encounter_type, encounter_date, status
- **Indexes**: patient_id, doctor_id, encounter_date, type, status

#### encounter_vitals
Vital signs recording
- **Primary Key**: vital_id
- **Foreign Keys**: encounter_id → encounters
- **Key Fields**: temperature, blood_pressure, heart_rate, oxygen_saturation, bmi

#### encounter_diagnoses
Diagnoses per encounter
- **Primary Key**: diagnosis_id
- **Foreign Keys**: encounter_id → encounters, icd_code_id → icd_codes
- **Key Fields**: diagnosis_type (primary/secondary), severity

#### encounter_procedures
Procedures performed during encounter
- **Primary Key**: procedure_id
- **Foreign Keys**: encounter_id → encounters, cpt_code_id → cpt_codes, room_id → rooms
- **Key Fields**: procedure_datetime, anesthesia_type, outcome

#### clinical_notes
Progress notes and documentation
- **Primary Key**: note_id
- **Foreign Keys**: encounter_id → encounters
- **Key Fields**: note_type, author_id, author_type, is_signed

#### bed_assignments
Patient bed assignments
- **Primary Key**: assignment_id
- **Foreign Keys**: patient_id → patients, bed_id → beds, encounter_id → encounters
- **Key Fields**: assignment_datetime, status

---

### 7. Laboratory & Diagnostics (5 tables)

#### lab_orders
Laboratory test orders
- **Primary Key**: order_id
- **Unique**: order_number
- **Foreign Keys**: encounter_id → encounters, patient_id → patients, ordering_doctor_id → doctors
- **Key Fields**: order_datetime, priority, status

#### lab_tests
Individual tests per order
- **Primary Key**: test_id
- **Foreign Keys**: order_id → lab_orders
- **Key Fields**: test_code, test_name, specimen_type

#### lab_results
Test results with reference ranges
- **Primary Key**: result_id
- **Foreign Keys**: test_id → lab_tests
- **Key Fields**: result_value, abnormal_flag, verified_by

#### radiology_orders
Imaging study orders
- **Primary Key**: order_id
- **Unique**: order_number
- **Foreign Keys**: encounter_id → encounters, patient_id → patients, ordering_doctor_id → doctors
- **Key Fields**: exam_type, modality, scheduled_datetime

#### radiology_results
Radiology findings and reports
- **Primary Key**: result_id
- **Foreign Keys**: order_id → radiology_orders, radiologist_id → doctors
- **Key Fields**: findings, impression, critical_findings

---

### 8. Pharmacy & Medications (6 tables)

#### medications
Drug formulary
- **Primary Key**: medication_id
- **Unique**: ndc_code
- **Key Fields**: generic_name, drug_class, dosage_form, strength
- **Indexes**: medication_name, generic_name, ndc_code, drug_class

#### drug_interactions
Drug-drug interactions
- **Primary Key**: interaction_id
- **Foreign Keys**: medication_id_1 → medications, medication_id_2 → medications
- **Unique**: (medication_id_1, medication_id_2)
- **Key Fields**: interaction_type, description

#### prescriptions
Electronic prescriptions
- **Primary Key**: prescription_id
- **Unique**: prescription_number
- **Foreign Keys**: encounter_id → encounters, patient_id → patients, doctor_id → doctors, medication_id → medications
- **Key Fields**: dosage, route, frequency, refills_remaining
- **Indexes**: encounter_id, patient_id, doctor_id, medication_id, status

#### prescription_refills
Refill tracking
- **Primary Key**: refill_id
- **Foreign Keys**: prescription_id → prescriptions
- **Key Fields**: refill_date, quantity_dispensed, pharmacy_name

#### medication_inventory
Stock management
- **Primary Key**: inventory_id
- **Foreign Keys**: medication_id → medications
- **Key Fields**: lot_number, expiration_date, quantity_on_hand, reorder_level

#### pharmacy_orders
Inventory replenishment
- **Primary Key**: order_id
- **Unique**: order_number
- **Foreign Keys**: medication_id → medications
- **Key Fields**: supplier_name, order_date, quantity_ordered, order_status

---

### 9. Insurance & Billing (7 tables)

#### insurance_companies
Insurance provider directory
- **Primary Key**: insurance_company_id
- **Unique**: company_name, company_code
- **Key Fields**: phone, email, is_active

#### insurance_plans
Insurance plan details
- **Primary Key**: plan_id
- **Foreign Keys**: insurance_company_id → insurance_companies
- **Key Fields**: plan_type, deductible_amount, copay_amount

#### patient_insurance_policies
Patient coverage
- **Primary Key**: policy_id
- **Foreign Keys**: patient_id → patients, insurance_plan_id → insurance_plans
- **Key Fields**: policy_number, is_primary, status

#### insurance_authorizations
Pre-authorizations
- **Primary Key**: authorization_id
- **Unique**: authorization_number
- **Foreign Keys**: patient_id → patients, policy_id → patient_insurance_policies, cpt_code_id → cpt_codes
- **Key Fields**: units_authorized, status

#### insurance_claims
Claims submission and tracking
- **Primary Key**: claim_id
- **Unique**: claim_number
- **Foreign Keys**: patient_id → patients, policy_id → patient_insurance_policies, encounter_id → encounters
- **Key Fields**: total_charge, paid_amount, status
- **Indexes**: patient_id, policy_id, encounter_id, status, claim_date

#### insurance_claim_items
Itemized claim details
- **Primary Key**: claim_item_id
- **Foreign Keys**: claim_id → insurance_claims, cpt_code_id → cpt_codes, icd_code_id → icd_codes
- **Key Fields**: service_date, quantity, unit_charge

#### invoices
Patient billing
- **Primary Key**: invoice_id
- **Unique**: invoice_number
- **Foreign Keys**: patient_id → patients, encounter_id → encounters
- **Key Fields**: total_amount, amount_paid, payment_status
- **Computed**: amount_due (total_amount - amount_paid)
- **Indexes**: patient_id, encounter_id, payment_status, invoice_date

---

### 10. Payment Processing (2 tables)

#### invoice_items
Itemized charges
- **Primary Key**: item_id
- **Foreign Keys**: invoice_id → invoices, cpt_code_id → cpt_codes
- **Key Fields**: item_type, quantity, unit_price, total_price

#### payment_transactions
Payment processing
- **Primary Key**: transaction_id
- **Unique**: transaction_number
- **Foreign Keys**: invoice_id → invoices, patient_id → patients
- **Key Fields**: payment_date, payment_amount, payment_method, status

---

### 11. System Administration (4 tables)

#### users
System user accounts
- **Primary Key**: user_id
- **Unique**: username, email
- **Key Fields**: user_type, reference_id, is_active, last_login
- **Indexes**: username, email, user_type

#### roles
Role definitions
- **Primary Key**: role_id
- **Unique**: role_name
- **Key Fields**: permissions (JSON format)

#### user_roles
Role assignments
- **Primary Key**: user_role_id
- **Foreign Keys**: user_id → users, role_id → roles
- **Unique**: (user_id, role_id)

#### audit_logs
Comprehensive audit trail
- **Primary Key**: log_id
- **Key Fields**: table_name, record_id, action, user_id, old_values, new_values
- **Indexes**: table_name, record_id, user_id, action, timestamp
- **Purpose**: Track all data changes for compliance

---

## Key Relationships

### Patient Flow
```
patients → patient_addresses
         → patient_emergency_contacts
         → patient_allergies
         → patient_insurance_policies
         → appointments → encounters → encounter_vitals
                                    → encounter_diagnoses
                                    → encounter_procedures
                                    → clinical_notes
                       → lab_orders → lab_tests → lab_results
                       → radiology_orders → radiology_results
                       → prescriptions → prescription_refills
         → invoices → invoice_items
                   → payment_transactions
         → insurance_claims → insurance_claim_items
```

### Provider Management
```
departments → doctors → specialists
                     → doctor_schedules
                     → appointments
                     → encounters
                     → prescriptions
            → nurses → nurse_assignments
                    → staff_shifts
            → staff → staff_shifts
```

### Facility Management
```
facilities → rooms → beds → bed_assignments
                  → appointments
                  → encounters
```

## Database Views (15+ views)

1. **vw_active_doctors** - Active doctors with department info
2. **vw_patient_summary** - Patient overview with encounter statistics
3. **vw_upcoming_appointments** - Future scheduled appointments
4. **vw_todays_appointments** - Today's appointment schedule
5. **vw_active_encounters** - In-progress patient encounters
6. **vw_outstanding_invoices** - Unpaid invoices with aging
7. **vw_pending_lab_orders** - Lab orders in progress
8. **vw_pending_radiology_orders** - Radiology orders pending
9. **vw_active_prescriptions** - Current patient prescriptions
10. **vw_available_beds** - Available bed inventory
11. **vw_bed_occupancy** - Current bed occupancy
12. **vw_low_stock_medications** - Low stock alerts
13. **vw_insurance_claims_summary** - Claims status overview
14. **vw_doctor_performance** - Doctor productivity metrics
15. **vw_department_statistics** - Department resource summary

## Index Strategy

### High-Performance Indexes
- All foreign keys are indexed
- Patient MRN (unique identifier)
- Appointment date and status
- Encounter date and type
- Doctor NPI number
- Medication NDC code
- Invoice payment status

### Composite Indexes
- Patient name (last_name, first_name)
- Appointment (date, time)
- Unique constraints on natural keys

## Data Integrity

### Referential Integrity
- All foreign keys use ON DELETE CASCADE or ON DELETE SET NULL appropriately
- ON DELETE RESTRICT for reference data (ICD, CPT codes)

### Data Validation
- ENUM types for standardized values
- NOT NULL constraints on required fields
- UNIQUE constraints on business identifiers
- CHECK constraints where supported

### Audit Trail
- All tables have created_at timestamp
- Most tables have updated_at timestamp
- audit_logs table tracks all critical changes

## Performance Considerations

### Optimization Features
- Generated/computed columns (e.g., amount_due, age)
- Selective indexes on frequently queried columns
- Views for complex queries
- Proper data types for storage efficiency

### Scalability
- Partitioning candidates: audit_logs, payment_transactions (by date)
- Archive strategy for historical data
- Efficient join paths through proper normalization

## Security & Compliance

### HIPAA Compliance Ready
- Audit logging for all access
- User authentication and authorization
- Role-based access control
- Encrypted sensitive data fields (implement at application level)

### PHI Protection
- Patient identifiers tracked
- Access logging in audit_logs
- User activity monitoring

---

## Quick Reference

**Total Tables**: 50
**Total Views**: 15+
**Total Indexes**: 100+ (including foreign keys)
**Relationships**: 80+ foreign key constraints
**Database Engine**: MySQL/MariaDB
**Character Set**: UTF-8
**Collation**: utf8mb4_general_ci

---

*Last Updated: 2026-02-12*
