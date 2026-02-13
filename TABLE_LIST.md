# Hospital OLTP System - Complete Table List

## Total: 50 Tables

### Reference & Lookup Tables (2)
1. `icd_codes` - International Classification of Diseases codes
2. `cpt_codes` - Current Procedural Terminology codes

### Organizational Structure (6)
3. `departments` - Hospital departments
4. `facilities` - Buildings and physical structures
5. `rooms` - Individual rooms
6. `beds` - Bed inventory
7. `equipment` - Medical equipment
8. `department_equipment` - Equipment assignments

### Patient Information (4)
9. `patients` - Core patient records
10. `patient_addresses` - Patient addresses
11. `patient_emergency_contacts` - Emergency contacts
12. `patient_allergies` - Allergy tracking

### Healthcare Providers (8)
13. `doctors` - Medical doctors
14. `nurses` - Nursing staff
15. `staff` - Administrative staff
16. `specialists` - Consulting specialists
17. `nurse_assignments` - Patient assignments
18. `staff_shifts` - Shift schedules
19. `doctor_schedules` - Doctor availability

### Appointments & Scheduling (3)
20. `appointment_types` - Appointment categories
21. `appointments` - Appointment scheduling
22. `appointment_cancellations` - Cancellation tracking

### Clinical Encounters (6)
23. `encounters` - Patient visits
24. `encounter_vitals` - Vital signs
25. `encounter_diagnoses` - Diagnoses per visit
26. `encounter_procedures` - Procedures performed
27. `clinical_notes` - Clinical documentation
28. `bed_assignments` - Patient bed assignments

### Laboratory & Diagnostics (5)
29. `lab_orders` - Laboratory test orders
30. `lab_tests` - Individual tests
31. `lab_results` - Test results
32. `radiology_orders` - Imaging orders
33. `radiology_results` - Imaging results

### Pharmacy & Medications (6)
34. `medications` - Drug formulary
35. `drug_interactions` - Drug interactions
36. `prescriptions` - Electronic prescriptions
37. `prescription_refills` - Refill tracking
38. `medication_inventory` - Stock levels
39. `pharmacy_orders` - Inventory orders

### Insurance (7)
40. `insurance_companies` - Insurance providers
41. `insurance_plans` - Insurance plans
42. `patient_insurance_policies` - Patient coverage
43. `insurance_authorizations` - Pre-authorizations
44. `insurance_claims` - Claims submission
45. `insurance_claim_items` - Claim line items

### Billing & Payments (3)
46. `invoices` - Patient invoices
47. `invoice_items` - Invoice line items
48. `payment_transactions` - Payment processing

### System Administration (4)
49. `users` - System users
50. `roles` - Role definitions
51. `user_roles` - User-role assignments
52. `audit_logs` - Audit trail

**Note**: Actually 52 tables total (50+ requirement met)

## Database Views (15+)

1. `vw_active_doctors` - Active doctors with department info
2. `vw_patient_summary` - Patient overview with statistics
3. `vw_upcoming_appointments` - Future appointments
4. `vw_todays_appointments` - Today's schedule
5. `vw_active_encounters` - In-progress encounters
6. `vw_outstanding_invoices` - Unpaid invoices
7. `vw_pending_lab_orders` - Lab orders pending
8. `vw_pending_radiology_orders` - Radiology pending
9. `vw_active_prescriptions` - Current prescriptions
10. `vw_available_beds` - Available bed inventory
11. `vw_bed_occupancy` - Current occupancy
12. `vw_low_stock_medications` - Low stock alerts
13. `vw_insurance_claims_summary` - Claims overview
14. `vw_doctor_performance` - Performance metrics
15. `vw_department_statistics` - Department stats

## Key Features

### Primary Key Strategy
- All tables use `AUTO_INCREMENT` integer primary keys
- Naming convention: `{table_name}_id`

### Foreign Key Constraints
- 80+ foreign key relationships
- Cascading deletes where appropriate
- SET NULL for optional references
- RESTRICT for reference data

### Indexes
- 100+ indexes total
- All foreign keys indexed
- Business keys have unique constraints
- Composite indexes on frequently searched combinations

### Data Types
- **VARCHAR** for variable-length strings with appropriate limits
- **TEXT** for long-form content (notes, descriptions)
- **ENUM** for predefined value lists
- **DECIMAL** for monetary values
- **DATE/DATETIME/TIME/TIMESTAMP** for temporal data
- **BOOLEAN** for flags
- **INT** for counts and IDs

### Constraints
- NOT NULL on required fields
- UNIQUE on business identifiers (MRN, license numbers, etc.)
- CHECK constraints (where supported)
- DEFAULT values for common scenarios
- Generated/computed columns

### Audit Trail
- `created_at` timestamp on all tables
- `updated_at` timestamp on most tables (auto-updated)
- `audit_logs` table for comprehensive change tracking

### Status Fields
Most major tables include status tracking:
- **active/inactive** for most entities
- **scheduled/in_progress/completed/cancelled** for workflows
- **pending/partial/paid** for financial transactions

## Query Performance Features

### Optimized for Common Queries
- Patient lookup by MRN, name, or DOB
- Doctor lookup by NPI, name, or specialization
- Appointment scheduling and conflicts
- Medication lookup by name or NDC
- Insurance verification
- Outstanding balances
- Lab/radiology results retrieval

### Materialized Views (Use Views)
Complex aggregations pre-computed for:
- Department statistics
- Doctor performance metrics
- Patient summaries
- Outstanding invoices with aging

### Partitioning Candidates
For large-scale deployments, consider partitioning:
- `audit_logs` by timestamp (monthly/yearly)
- `payment_transactions` by payment_date
- `lab_results`, `radiology_results` by date
- Historical `encounters` by encounter_date

## Data Volume Estimates

### High-Volume Tables (Growth Rate)
- `audit_logs` - Very high (every action)
- `lab_results` - High (per test)
- `payment_transactions` - Medium-high
- `clinical_notes` - Medium-high
- `encounter_vitals` - Medium

### Medium-Volume Tables
- `appointments` - Medium (daily operations)
- `encounters` - Medium (daily operations)
- `prescriptions` - Medium (per encounter)
- `invoices` - Medium (per encounter)

### Low-Volume Tables
- `patients` - Low (cumulative growth)
- `doctors` - Very low (staff changes)
- `medications` - Very low (formulary updates)
- `insurance_companies` - Very low (rarely changes)

## Security Considerations

### Sensitive Data Tables
- `patients` - PHI (Protected Health Information)
- `patient_addresses` - Personal information
- `patient_allergies` - Medical information
- `encounters` and all related clinical data
- `prescriptions` - Prescription records
- `insurance_policies` - Insurance info
- `payment_transactions` - Financial data

### Access Control
- Role-based access via `users`, `roles`, `user_roles`
- Audit logging for all access to sensitive data
- Consider encryption at rest for PHI
- Use application-level encryption for SSN, credit card data

### HIPAA Compliance
- Comprehensive audit trail in `audit_logs`
- Access tracking for all PHI
- Emergency access protocols
- Data retention policies
- Breach notification procedures

## Backup Strategy

### Critical Tables (Backup Frequently)
- All clinical data (encounters, diagnoses, procedures)
- Patient information
- Prescriptions
- Appointments
- Financial transactions

### Reference Data (Backup Less Frequently)
- ICD/CPT codes
- Medications
- Insurance companies/plans
- Department/facility info

### System Data
- Users, roles (include in regular backups)
- Audit logs (consider separate archive)

## Maintenance Tasks

### Regular Maintenance
- Update statistics weekly
- Rebuild indexes monthly
- Archive old audit logs (> 1 year)
- Archive completed encounters (> 2 years)
- Verify referential integrity monthly

### Data Cleanup
- Purge cancelled appointments (> 30 days)
- Archive inactive patients (configurable)
- Clean up expired medication inventory
- Remove old audit logs per retention policy

---

**Database Statistics:**
- Tables: 52
- Views: 15+
- Foreign Keys: 80+
- Indexes: 100+
- Constraints: 150+

**Estimated Database Size (10,000 patients):**
- Small deployment: 5-10 GB
- Medium deployment: 50-100 GB
- Large deployment: 500+ GB (with full history)

*Last Updated: 2026-02-12*
