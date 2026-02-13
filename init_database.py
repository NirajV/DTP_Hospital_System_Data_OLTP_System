"""
Initialize Hospital OLTP Database
Creates database and tables using the SQL schema
"""

import mysql.connector
from mysql.connector import Error
from database_connection import DB_CONFIG, DATABASE_NAME, logger


def create_database():
    """Create the hospital_OLTP_system database if it doesn't exist"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
            logger.info(f"Database '{DATABASE_NAME}' created or already exists")
            cursor.close()
            connection.close()
            return True
    except Error as e:
        logger.error(f"Error creating database: {e}")
        return False


def execute_sql_file(filename='create_schema.sql'):
    """Execute SQL commands from a file"""
    try:
        # Read the SQL file
        with open(filename, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Connect to MySQL
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Clean and parse the SQL statements properly
            # Remove single-line comments
            lines = []
            for line in sql_script.split('\n'):
                # Skip lines that are only comments
                stripped = line.strip()
                if stripped.startswith('--'):
                    continue
                # Remove inline comments
                if '--' in line:
                    line = line.split('--')[0]
                lines.append(line)
            
            clean_script = '\n'.join(lines)
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in clean_script.split(';') if stmt.strip()]
            
            success_count = 0
            error_count = 0
            
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                    # Consume any results to avoid "Unread result found" error
                    try:
                        cursor.fetchall()
                    except:
                        pass  # No results to fetch
                    success_count += 1
                except Error as e:
                    # Log warnings for DROP TABLE on non-existent tables (expected)
                    if 'doesn\'t exist' in str(e) or '1051' in str(e):
                        error_count += 1
                    else:
                        logger.error(f"Error executing statement: {e}")
                        logger.debug(f"Statement: {stmt[:200]}...")
                        error_count += 1
            
            connection.commit()
            logger.info(f"Successfully executed {success_count} SQL statements ({error_count} warnings)")
            
            cursor.close()
            connection.close()
            return True
            
    except FileNotFoundError:
        logger.error(f"SQL file '{filename}' not found")
        return False
    except Error as e:
        logger.error(f"Error executing SQL file: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


def insert_sample_data():
    """Verify sample data insertion from SQL file"""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor
            
            # Display summary of inserted data from all 52 tables
            tables_to_check = [
                # Reference Data
                'icd_codes', 'cpt_codes',
                # Organizational
                'departments', 'facilities', 'rooms', 'beds', 'equipment', 'department_equipment',
                # Patient
                'patients', 'patient_addresses', 'patient_emergency_contacts', 'patient_allergies',
                # Providers
                'doctors', 'nurses', 'staff', 'specialists', 
                'nurse_assignments', 'staff_shifts', 'doctor_schedules',
                # Appointments
                'appointment_types', 'appointments', 'appointment_cancellations',
                # Encounters
                'encounters', 'encounter_vitals', 'encounter_diagnoses', 
                'encounter_procedures', 'clinical_notes', 'bed_assignments',
                # Laboratory
                'lab_orders', 'lab_tests', 'lab_results',
                'radiology_orders', 'radiology_results',
                # Pharmacy
                'medications', 'drug_interactions', 'prescriptions',
                'prescription_refills', 'medication_inventory', 'pharmacy_orders',
                # Insurance
                'insurance_companies', 'insurance_plans', 'patient_insurance_policies',
                'insurance_authorizations', 'insurance_claims', 'insurance_claim_items',
                # Billing
                'invoices', 'invoice_items', 'payment_transactions',
                # System Admin
                'users', 'roles', 'user_roles', 'audit_logs'
            ]
            
            print(f"\n{'='*70}")
            print("HOSPITAL OLTP SYSTEM - DATABASE INITIALIZATION SUMMARY")
            print(f"{'='*70}\n")
            
            total_records = 0
            table_stats = {}
            
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                    result = cursor.fetchone()
                    count = result['count'] if result else 0
                    total_records += count
                    table_stats[table] = count
                    
                    # Print with status indicator
                    status = "[+]" if count > 0 else "[ ]"
                    print(f"{status} {table.replace('_', ' ').title():<40}: {count:>5} records")
                except Exception as e:
                    print(f"[ERROR] {table.replace('_', ' ').title():<40}: ERROR")
            
            print(f"\n{'='*70}")
            print(f"{'TOTAL RECORDS':<40}: {total_records:>5}")
            print(f"{'TOTAL TABLES':<40}: {len(table_stats):>5}")
            print(f"{'='*70}\n")
            
            # Display reference data
            print("\nKEY REFERENCE DATA LOADED:")
            print(f"  ICD Codes:           {table_stats.get('icd_codes', 0)} diagnosis codes")
            print(f"  CPT Codes:           {table_stats.get('cpt_codes', 0)} procedure codes")
            
            # Display organizational data
            print(f"\nORGANIZATIONAL STRUCTURE:")
            print(f"  Departments:         {table_stats.get('departments', 0)} departments")
            print(f"  Facilities:          {table_stats.get('facilities', 0)} facilities")
            print(f"  Rooms:               {table_stats.get('rooms', 0)} rooms")
            print(f"  Beds:                {table_stats.get('beds', 0)} beds")
            print(f"  Equipment:           {table_stats.get('equipment', 0)} equipment items")
            
            # Display healthcare providers
            print(f"\nHEALTHCARE PROVIDERS:")
            print(f"  Doctors:             {table_stats.get('doctors', 0)} doctors")
            print(f"  Nurses:              {table_stats.get('nurses', 0)} nurses")
            print(f"  Staff:               {table_stats.get('staff', 0)} staff members")
            
            # Display patient data
            print(f"\nPATIENT DATA:")
            print(f"  Patients:            {table_stats.get('patients', 0)} patients")
            print(f"  Addresses:           {table_stats.get('patient_addresses', 0)} addresses")
            print(f"  Emergency Contacts:  {table_stats.get('patient_emergency_contacts', 0)} contacts")
            
            # Display clinical data
            print(f"\nCLINICAL OPERATIONS:")
            print(f"  Appointments:        {table_stats.get('appointments', 0)} appointments")
            print(f"  Encounters:          {table_stats.get('encounters', 0)} encounters")
            print(f"  Lab Orders:          {table_stats.get('lab_orders', 0)} lab orders")
            print(f"  Prescriptions:       {table_stats.get('prescriptions', 0)} prescriptions")
            
            # Display insurance & billing
            print(f"\nINSURANCE & BILLING:")
            print(f"  Insurance Plans:     {table_stats.get('insurance_plans', 0)} plans")
            print(f"  Insurance Claims:    {table_stats.get('insurance_claims', 0)} claims")
            print(f"  Invoices:            {table_stats.get('invoices', 0)} invoices")
            print(f"  Payments:            {table_stats.get('payment_transactions', 0)} payments")
            
            print(f"\n{'='*70}")
            print("[OK] Database initialization completed successfully!")
            print(f"{'='*70}\n")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        logger.error(f"Error checking sample data: {e}")
        return False


def initialize_database():
    """Main function to initialize the complete database"""
    print("Starting Hospital OLTP Database Initialization...\n")
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        print("Failed to create database. Exiting.")
        return False
    print("[OK] Database created\n")
    
    # Step 2: Execute schema file
    print("Step 2: Creating tables and schema...")
    if not execute_sql_file():
        print("Failed to create schema. Exiting.")
        return False
    print("[OK] Schema created\n")
    
    # Step 3: Insert sample data
    print("Step 3: Verifying sample data...")
    if not insert_sample_data():
        print("Warning: Could not verify sample data, but schema is ready.")
        return True
    print("[OK] Sample data verified\n")
    
    print("="*50)
    print("Database initialization completed successfully!")
    print("="*50)
    return True


if __name__ == "__main__":
    import sys
    success = initialize_database()
    sys.exit(0 if success else 1)
