# Hospital OLTP Database System

A comprehensive Hospital OLTP (Online Transaction Processing) database system built with MySQL, supporting 52 interconnected tables across all hospital operational domains with complete fake data loading and timestamped logging capabilities.

## 🎯 Overview

This enterprise-grade hospital management database implements:
- **52 Tables** with complete domain coverage
- **82 Foreign Key Relationships** ensuring data integrity
- **15 Database Views** for reporting and analytics
- **500+ Test Records** via comprehensive fake data loaders
- **Timestamped Logging** for audit trails (Prompts 22-23)
- **Production-Ready Schema** with proper indexing and constraints

## 🏥 Domain Organization

| Domain | Tables | Description |
|--------|--------|-------------|
| **Reference Data** | 2 | ICD-10 and CPT coding standards |
| **Organizational** | 6 | Departments, facilities, rooms, beds, equipment |
| **Patients** | 4 | Patient records, addresses, contacts, allergies |
| **Providers** | 7 | Doctors, nurses, staff, specialists, schedules |
| **Appointments** | 3 | Appointment types, scheduling, cancellations |
| **Clinical** | 6 | Encounters, vitals, diagnoses, procedures, notes |
| **Laboratory** | 5 | Lab orders, tests, results, radiology |
| **Pharmacy** | 6 | Medications, prescriptions, inventory, interactions |
| **Insurance** | 7 | Companies, plans, policies, claims |
| **Billing** | 3 | Invoices, items, payment transactions |
| **System** | 4 | Users, roles, audit logging |

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
MySQL 8.0+
mysql-connector-python
```

### Installation & Initialization

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Initialize Database (Recommended)**
```bash
python init_database_Setup.py
```

This automatically:
- Creates `hospital_OLTP_system` database
- Creates all 52 tables (82 FK relationships)
- Loads 104 sample records
- Verifies all objects
- Creates timestamped log file in `init_database_Setup/` directory

3. **Load Comprehensive Fake Data** (Optional but recommended for testing)
```bash
python load_all_fake_data.py
```

This loads 5 data layers (500+ records total):
- **Layer 1:** Reference data (ICD codes, CPT codes, medications)
- **Layer 2:** Organizational data (departments, facilities, rooms, beds, equipment)
- **Layer 3:** Staff data (doctors, nurses, specialists, schedules)
- **Layer 4:** Patient data (patients, addresses, contacts, allergies)
- **Layer 5:** Transactional data (appointments, insurance policies)

Creates timestamped log in `Fake_Data_Log/` directory.

## 📁 Project Files

**Python Scripts:**
- `database_connection.py` - Database connection manager & logger
- `init_database_Setup.py` - Complete initialization (all-in-one)
- `load_all_fake_data.py` - Fake data loader (500+ records)

**SQL Files:**
- `create_schema.sql` - 52 tables with 82 FK constraints
- `database_views.sql` - 15 database views for reporting
- `hospital_sample_data.sql` - Sample data for initial setup
- `dml_*.sql` - Domain-specific DML files (optional)

**Documentation:**
- `README.md` - This file (overview & quick start)
- `SCHEMA_DOCUMENTATION.md` - Complete technical reference
- `ManMade_Prompts.txt` - Full development history (23 prompts)

**Directories:**
- `Fake_Data_Log/` - Timestamped logs from load_all_fake_data.py
- `init_database_Setup/` - Timestamped logs from init_database_Setup.py

## 🗄️ Database Architecture

### Schema Features

**Foreign Key Integrity:**
- 82 explicit FK constraints
- Proper CASCADE, SET NULL, and RESTRICT rules
- Prevents orphaned records

**Indexing:**
- Primary keys on all tables
- FK indexes for join performance
- Business keys (MRN, NPI, license numbers)
- Composite indexes on frequently searched columns

**Data Quality:**
- ENUM types for standardized values
- NOT NULL constraints on required fields
- UNIQUE constraints on business identifiers
- Computed columns for derived values

**Audit Trail:**
- `created_at` timestamp on all tables
- `updated_at` on most tables (auto-maintained)
- `audit_logs` table for comprehensive change tracking

### 15 Database Views

**Clinical Operations:** vw_active_doctors, vw_todays_appointments, vw_upcoming_appointments, vw_active_encounters, vw_active_prescriptions

**Facility Management:** vw_available_beds, vw_bed_occupancy, vw_department_statistics

**Pharmacy & Lab:** vw_pending_lab_orders, vw_pending_radiology_orders, vw_low_stock_medications

**Financial:** vw_outstanding_invoices, vw_insurance_claims_summary, vw_patient_summary

**Staff:** vw_doctor_performance

## 💾 Fake Data Features

### Comprehensive Test Data (500+ records)

**Reference Data (150+ records)**
- 54+ ICD-10 diagnosis codes
- 40+ CPT procedure codes  
- 40+ medications with interactions
- 10 insurance companies

**Organizational (104 records)**
- 12 departments
- 4 hospital facilities
- 31 rooms across buildings
- 33 beds
- 12 medical equipment items

**Staff (274 records)**
- 15 doctors with specializations
- 13 nurses with various licenses
- 8 administrative staff
- 8 consulting specialists
- 126 staff shift schedules
- 91 doctor weekly schedules

**Patients (183 records)**
- 15 diverse patient profiles
- 67 addresses (home, work, seasonal)
- 75 emergency contacts
- 26 allergies (drug, food, environmental)

### Automatic Logging

**Timestamped Logs:**
- `load_all_fake_data.py` → `Fake_Data_Log/load_all_fake_data_YYYYMMDD_HHMMSS.log`
- `init_database_Setup.py` → `init_database_Setup/init_database_Setup_YYYYMMDD_HHMMSS.log`
- All operations logged for audit trail and debugging

## 🔧 Usage Examples

### Initialize Database
```bash
python init_database_Setup.py
```

### Load Fake Data
```bash
python load_all_fake_data.py
```

### Python Connection
```python
from database_connection import DatabaseConnection

with DatabaseConnection() as db:
    results = db.execute_select(
        "SELECT * FROM vw_todays_appointments"
    )
    for appointment in results:
        print(f"Time: {appointment['appointment_time']}")
```

### Query Views
```bash
mysql -u root -p hospital_OLTP_system -e "SELECT * FROM vw_active_doctors;"
```

## 🔐 Security & Compliance

**HIPAA-Ready Design:**
- Comprehensive audit logging
- Role-based access control framework
- Protected Health Information (PHI) handling patterns
- User authentication and authorization tables

**Data Protection:**
- Sensitive field constraints (SSN, license numbers)
- Encrypted connection support
- Access logging for all critical operations

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Tables | 52 |
| Total Views | 15 |
| FK Relationships | 82 |
| Total Indexes | 100+ |
| Total Constraints | 150+ |
| Test Records | 500+ |
| Exit Code | 0 (success) |

## ✅ Project Status

**Completion:** 24 of 24 development prompts completed

**Latest Features:**
- ✅ Timestamped logging in load_all_fake_data.py (Prompt 22)
- ✅ Timestamped logging in init_database_Setup.py (Prompt 23)
- ✅ Markdown consolidation & cleanup (Prompt 24)

**Deliverables:**
- ✅ 52 tables with 82 FK relationships
- ✅ 15 database views
- ✅ Complete initialization system
- ✅ Fake data loader (500+ records)
- ✅ Timestamped audit logging
- ✅ Python scripts validated (Exit Code: 0)
- ✅ Business logic integrity verified
- ✅ Consolidated documentation (2 files only)

## 🎯 Use Cases

✅ Healthcare system testing  
✅ Database performance benchmarking  
✅ FK relationship validation  
✅ HIPAA compliance study  
✅ SQL optimization practice  
✅ Healthcare data analysis  
✅ Educational demonstrations  
✅ Portfolio projects  

## 📚 Related Documentation

- [SCHEMA_DOCUMENTATION.md](SCHEMA_DOCUMENTATION.md) - Complete technical reference with all table specifications
- [ManMade_Prompts.txt](ManMade_Prompts.txt) - Full development history and implementation details

---

**Status:** ✅ **PRODUCTION-READY**  
**Last Updated:** February 2026  
**Python:** 3.8+  
**MySQL:** 8.0+  
**Version:** 1.0 (Prompt 24 - Complete)
