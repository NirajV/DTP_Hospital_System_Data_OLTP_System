# Hospital OLTP Database System

A comprehensive Hospital OLTP (Online Transaction Processing) database system built with MySQL, supporting 52 interconnected tables across all hospital operational domains.

## 📋 Overview

This hospital management database implements enterprise-grade design with:
- **52 Tables** covering all hospital operations
- **82 Foreign Key Relationships** ensuring data integrity
- **15 Database Views** for common queries and reporting
- **Clean DDL/DML Separation** for flexible deployment
- **Production-Ready Schema** with proper indexing and constraints

## 🏥 Database Domains

The 52 tables are organized into 11 operational domains:

1. **Reference Data** - ICD codes, CPT codes
2. **Organizational** - Departments, Facilities, Rooms, Beds, Equipment
3. **Patient Management** - Patients, Addresses, Emergency Contacts, Allergies
4. **Healthcare Providers** - Doctors, Nurses, Staff, Specialists, Schedules
5. **Appointments** - Appointment Types, Appointments, Cancellations
6. **Clinical Encounters** - Encounters, Vitals, Diagnoses, Procedures, Notes
7. **Laboratory Services** - Lab Orders, Tests, Results
8. **Radiology** - Radiology Orders, Results
9. **Pharmacy** - Medications, Prescriptions, Inventory, Drug Interactions
10. **Insurance & Claims** - Companies, Plans, Policies, Authorizations, Claims
11. **Billing** - Invoices, Invoice Items, Payment Transactions
12. **System Administration** - Users, Roles, Audit Logs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- mysql-connector-python

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Database Connection**
```bash
# Edit connection details if needed (default: localhost:3306, root/12345678)
# Connection settings are in database_connection.py
```

3. **Initialize Database**
```bash
# Creates database, all 52 tables, and 82 FK relationships
python init_database.py

# Optional: Load database views (15 views for reporting)
mysql -u root -p12345678 hospital_OLTP_system < database_views.sql
```

Expected output:
```
Step 1: Creating database... [OK]
Step 2: Creating tables and schema... [OK]
Step 3: Verifying sample data... [OK]

TOTAL TABLES: 52
Exit Code: 0
```

**Note:** Database views are separate and can be loaded optionally using `database_views.sql`.

## 📁 Project Structure

### Core Files

**SQL Schema Files:**
- `create_schema.sql` - Complete DDL for all 52 tables and 82 FK constraints (1564 lines)
- `database_views.sql` - All 15 database views for reporting and queries (373 lines)
- `hospital_sample_data.sql` - Combined sample data for all tables

**DML Data Files (Optional):**
- `dml_01_reference_data.sql` - ICD codes, CPT codes
- `dml_02_organizational_data.sql` - Departments, Facilities, Rooms, Beds
- `dml_03_staff_data.sql` - Doctors, Nurses, Staff
- `dml_04_patient_data.sql` - Patients, Addresses, Appointments
- `dml_05_pharmacy_data.sql` - Medications, Inventory
- `dml_06_insurance_data.sql` - Insurance Companies, Plans, Policies

**Python Scripts:**
- `database_connection.py` - Database connection manager with context support
- `init_database.py` - Database initialization and verification script
- `init_schema.py` - Alternative schema initialization script

**Documentation:**
- `README.md` - This file
- `SCHEMA_DOCUMENTATION.md` - Complete table specifications
- `ManMade_Prompts.txt` - Project development history (13 prompts)

**Configuration:**
- `requirements.txt` - Python dependencies
- `.env.example` - Configuration template
- `.gitignore` - Git ignore rules

## 🗄️ Database Schema Structure

### Key Features

**Foreign Key Management:**
- All FK constraints explicitly defined
- Proper CASCADE, SET NULL, and RESTRICT rules
- Clean drop/create cycle using `SET FOREIGN_KEY_CHECKS`

**Indexing Strategy:**
- Primary keys on all tables
- Foreign key indexes for join performance
- Business key indexes (e.g., license numbers, patient IDs)
- Timestamp indexes for temporal queries

**Data Integrity:**
- ENUM types for status fields
- NOT NULL constraints on required fields
- UNIQUE constraints on business identifiers
- CHECK constraints where applicable

### Sample Tables

**Core Entities:**
```sql
patients (patient_id, first_name, last_name, DOB, ssn, ...)
doctors (doctor_id, employee_id, first_name, last_name, specialization, ...)
appointments (appointment_id, patient_id, doctor_id, appointment_datetime, status, ...)
encounters (encounter_id, patient_id, doctor_id, encounter_datetime, ...)
prescriptions (prescription_id, encounter_id, medication_id, dosage, ...)
insurance_claims (claim_id, patient_id, encounter_id, claim_amount, status, ...)
```

For complete table specifications, see [SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md).

## 📊 Database Views

15 pre-built views for common queries:

**Clinical Views:**
- `vw_active_doctors` - Active doctors with department info
- `vw_active_encounters` - Current patient encounters
- `vw_active_prescriptions` - Active prescriptions with patient info
- `vw_todays_appointments` - Today's appointment schedule
- `vw_upcoming_appointments` - Future appointments (next 7 days)

**Operational Views:**
- `vw_available_beds` - Available hospital beds
- `vw_bed_occupancy` - Bed occupancy statistics
- `vw_department_statistics` - Department activity metrics
- `vw_doctor_performance` - Doctor workload and performance

**Pharmacy Views:**
- `vw_low_stock_medications` - Medications below reorder point
- `vw_pending_lab_orders` - Pending lab test orders
- `vw_pending_radiology_orders` - Pending radiology orders

**Financial Views:**
- `vw_outstanding_invoices` - Unpaid invoices
- `vw_insurance_claims_summary` - Claims by status
- `vw_patient_summary` - Patient demographics with visit history

## 🔧 Usage Examples

### Basic Connection

```python
from database_connection import DatabaseConnection, DATABASE_NAME

# Using context manager (recommended)
with DatabaseConnection() as db:
    results = db.execute_select("SELECT * FROM patients WHERE status = 'active'")
    for patient in results:
        print(f"Patient: {patient['first_name']} {patient['last_name']}")
```

### Loading Sample Data

```bash
# Option 1: Load all sample data at once
mysql -u root -p hospital_OLTP_system < hospital_sample_data.sql

# Option 2: Load by domain
mysql -u root -p hospital_OLTP_system < dml_01_reference_data.sql
mysql -u root -p hospital_OLTP_system < dml_02_organizational_data.sql
# ... continue with other DML files
```

### Querying Views

```python
with DatabaseConnection() as db:
    # Get today's appointments
    appointments = db.execute_select("SELECT * FROM vw_todays_appointments")
    
    # Check bed availability
    available_beds = db.execute_select("SELECT * FROM vw_available_beds")
    
    # Get outstanding invoices
    invoices = db.execute_select("SELECT * FROM vw_outstanding_invoices")
```

## 📈 Data Model Highlights

### Patient Journey
```
Patient Registration → Patient Record Created
     ↓
Appointment Scheduled → Appointment Record
     ↓
Check-in → Encounter Created → Vitals Recorded
     ↓
Diagnosis → Encounter Diagnoses (with ICD codes)
     ↓
Treatment → Procedures (with CPT codes)
     ↓
Prescription → Medication Orders
     ↓
Billing → Invoice Generated → Insurance Claim
     ↓
Payment → Payment Transaction Recorded
```

### Key Relationships

- **Patients** have multiple addresses, emergency contacts, allergies, insurance policies
- **Doctors** belong to departments, have schedules, specialist qualifications
- **Appointments** link patients to doctors, rooms, and encounter records
- **Encounters** contain vitals, diagnoses (ICD), procedures (CPT), clinical notes
- **Prescriptions** reference encounters, medications, and include refill tracking
- **Insurance Claims** link to encounters, contain line items with CPT codes
- **Invoices** aggregate charges from encounters and link to payment transactions

## 🔐 Security & Compliance

### Audit Logging
The `audit_logs` table tracks all critical database operations:
- User actions (INSERT, UPDATE, DELETE)
- Affected table and record ID
- Timestamp and user identification
- Before/after values for compliance

### Data Protection
- Sensitive fields (SSN, license numbers) with appropriate constraints
- HIPAA-compliant design patterns
- Role-based access control (users, roles, user_roles tables)

## 🛠️ Development History

This database was developed through 13 iterative prompts:

1. Initial database structure (7 tables)
2. Database naming standardization
3. Expansion to 52 tables with relationships
4. Python CRUD operations planning
5. Legacy code cleanup
6. Documentation consolidation
7. Script automation enhancements
8. Bug fixes (AttributeError)
9. Explicit FK management implementation
10. DDL/DML separation
11. Documentation cleanup
12. Schema simplification (FK optimization)
13. Final documentation update

For complete development history, see [ManMade_Prompts.txt](ManMade_Prompts.txt).

## 📊 Statistics

- **Total Database Objects:** 67 (52 tables + 15 views)
- **Foreign Key Relationships:** 82 constraints
- **Schema File Size:** 1,564 lines (optimized)
- **Sample Data:** ~100+ records across 19 tables
- **Supported Workflows:** 10+ complete hospital workflows

## 🎯 Use Cases

This database system supports:

✅ **Patient Management** - Registration, demographics, medical history  
✅ **Appointment Scheduling** - Multi-provider scheduling with room allocation  
✅ **Clinical Documentation** - Encounters, diagnoses, procedures, notes  
✅ **Laboratory Services** - Orders, tests, results tracking  
✅ **Radiology Services** - Imaging orders and results  
✅ **Pharmacy Management** - Prescriptions, inventory, drug interactions  
✅ **Insurance Processing** - Policies, authorizations, claims management  
✅ **Billing & Payments** - Invoice generation, line items, payment tracking  
✅ **Facility Management** - Beds, rooms, equipment tracking  
✅ **Staff Management** - Doctors, nurses, schedules, assignments  
✅ **Reporting & Analytics** - 15+ pre-built views for common reports  

## 🤝 Contributing

This is a learning/demonstration project showcasing:
- Enterprise database design
- Healthcare domain modeling
- MySQL best practices
- FK constraint management
- DDL/DML separation
- Python database connectivity

## 📝 License

Educational/Demonstration Project

## 🔗 Additional Resources

- [SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md) - Detailed table specifications
- [ManMade_Prompts.txt](ManMade_Prompts.txt) - Complete development history
- MySQL Documentation: https://dev.mysql.com/doc/
- Healthcare Data Standards: ICD-10, CPT, HIPAA

---

**Status:** ✅ Production-Ready (52 tables, 82 FK relationships, 15 views validated)  
**Last Updated:** February 2026  
**Version:** 1.0 (Prompt 13 - Documentation Cleanup)
