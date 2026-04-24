# CLAUDE.md — DTP Hospital OLTP System

## Project Overview
Enterprise hospital OLTP (Online Transaction Processing) database system with 52 tables across 11 domains, 82 foreign key relationships, 15 database views, and 500+ test records. MySQL 8.0+ backend with Python initialization scripts.

## Tech Stack
- **Database:** MySQL 8.0+
- **Language:** Python 3.8+, SQL
- **Driver:** mysql-connector-python 8.3.0
- **DB Config:** Host=127.0.0.1, Port=3306, User=root, DB=hospital_OLTP_system

## Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (creates DB, 52 tables, loads 104 sample records)
python init_database_Setup.py

# Load comprehensive fake data (500+ records across 5 layers)
python load_all_fake_data.py

# Verify database
mysql -u root -p hospital_OLTP_system -e "SELECT * FROM vw_active_doctors;"
```

## Project Structure
```
├── database_connection.py        # DB connection manager (context manager pattern)
├── init_database_Setup.py        # One-time DB initialization script
├── load_all_fake_data.py         # Fake data loader (5-layer dependency-aware)
├── create_schema.sql             # 52 tables with 82 FK constraints
├── database_views.sql            # 15 reporting views
├── hospital_sample_data.sql      # Sample data inserts
├── dml_01_reference_data.sql     # ICD-10 & CPT codes
├── dml_02_organizational_data.sql # Departments, facilities, rooms
├── dml_03_staff_data.sql         # Doctors, nurses, staff
├── dml_04_patient_data.sql       # Patient records
├── dml_05_pharmacy_data.sql      # Medications
├── dml_06_insurance_data.sql     # Insurance data
├── requirements.txt              # Python dependencies
├── .env.example                  # DB config template
├── init_database_Setup/          # Init log files
├── Fake_Data_Log/                # Data loading log files
├── README.md                     # Project overview & quick start
├── SCHEMA_DOCUMENTATION.md       # Complete technical reference
└── ER_DIAGRAM.md                 # Entity relationship diagrams
```

## Database Domains (11)
1. **Reference Data** (2 tables) — ICD-10 diagnoses, CPT procedures
2. **Organizational** (6 tables) — Departments, facilities, rooms, beds, equipment
3. **Patients** (4 tables) — Patients, addresses, emergency contacts, allergies
4. **Providers** (8 tables) — Doctors, nurses, staff, specialists, schedules
5. **Appointments** (3 tables) — Types, appointments, cancellations
6. **Clinical** (6 tables) — Encounters, vitals, diagnoses, procedures, notes, bed assignments
7. **Laboratory** (5 tables) — Lab orders, tests, results, radiology
8. **Pharmacy** (6 tables) — Medications, interactions, prescriptions, inventory
9. **Insurance** (7 tables) — Companies, plans, policies, claims
10. **Billing** (3 tables) — Invoices, items, payment transactions
11. **System** (4 tables) — Users, roles, user roles, audit logs

## Code Conventions
- Python scripts use `logging` module with timestamped log files
- Database queries use parameterized statements (SQL injection prevention)
- `DatabaseConnection` class uses context manager pattern (`with` statement)
- Data loading follows dependency order: Reference → Organizational → Staff → Patients → Transactions
- All tables include `created_at` timestamps; most include `updated_at` (auto-maintained)
- ENUM types used for standardized values (status, gender, types)
- UNIQUE constraints on business identifiers (MRN, NPI, email, license numbers)

## Important Notes
- DB credentials are hardcoded in `database_connection.py` (not using .env at runtime)
- Log directories (`init_database_Setup/`, `Fake_Data_Log/`) are auto-created by scripts
- Schema uses CASCADE, SET NULL, and RESTRICT FK rules for referential integrity
- HIPAA-compliance ready with audit logging and RBAC framework
- `load_all_fake_data.py` is the largest file (~103 KB) with inline data generation
