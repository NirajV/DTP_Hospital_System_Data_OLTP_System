# Hospital OLTP System - Entity Relationship Diagrams

This document provides comprehensive visual representations of the database schema relationships across all domains.

## 1. High-Level System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HOSPITAL OLTP SYSTEM - 52 TABLES                      │
│                           (11 Domains)                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────┬───────────┬───┼───┬──────────┬────────────┐
        │           │           │   │   │          │            │
    ┌───▼──┐  ┌────▼───┐  ┌───▼──┐ │ ┌─▼───┐ ┌──▼────┐  ┌────▼──┐
    │PATIENTS│  │PROVIDERS│  │ORG │ │ │LABS│ │PHARMACY│  │INSURANCE│
    │(4)    │  │(7)     │  │(6) │ │ │(5) │ │(6)   │  │(7)     │
    └───┬──┘  └────┬───┘  └───┬──┘ │ └─┬───┘ └──┬────┘  └────┬──┘
        │          │          │    │   │        │            │
        │      ┌────┴──┐      │    │   │    ┌───┴─┐       ┌──┴────┐
        │      │       │      │    │   │    │     │       │       │
    ┌───▼──────▼──┐ ┌──▼─────▼──┐ ├───┼────┤  ┌──▼───┐  ┌─▼──┐
    │APPOINTMENTS │ │ ENCOUNTERS │ │   │    │  │BILLING│  │SYS │
    │(3)          │ │(6)         │ │   │    │  │(3)    │  │(4) │
    └──────────────┘ └────────────┘ │   │    │  └───────┘  └─────┘
                                     │   │    │
                          REFERENCE DATA
                             (2)
```

## 2. Reference Data Domain

```
┌──────────────────────────────────────┐
│         REFERENCE DATA (2)           │
├──────────────────────────────────────┤
│ • icd_codes (54+ diagnosis codes)    │
│ • cpt_codes (40+ procedure codes)    │
└──────────────────────────────────────┘
         ▲              ▲
         │              │
    Referenced by:
    • encounter_diagnoses (icd_code_id)
    • encounter_procedures (cpt_code_id)
    • insurance_claim_items (icd/cpt)
```

## 3. Organizational Structure Domain

```
        ┌─────────────────────────────────────────────┐
        │     ORGANIZATIONAL STRUCTURE (6)             │
        └─────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼─────┐    ┌─────▼────┐    ┌────▼────┐
   │departments│    │facilities │    │equipment│
   │(12)      │    │(4)        │    │(12)     │
   └────┬─────┘    └─────┬────┘    └────────┘
        │                │
        │ 1:N            │ 1:N
        │                │
   ┌────▼──────────┐     │
   │   rooms       │     │
   │   (31)        │     │
   └────┬──────────┘     │
        │ 1:N            │
        │                │
   ┌────▼──────────┐     │
   │    beds       │     │
   │   (33)        │     │
   └───────────────┘     │
                         │
                    ┌────▼──────────────┐
                    │department_equipment│
                    │(12)               │
                    └───────────────────┘
                    
Relationships:
- facilities 1 ──────────────> N rooms
- rooms 1 ──────────────> N beds
- departments 1 ──────────────> N doctors
- departments 1 ──────────────> N nurses
- departments 1 ──────────────> N staff
- departments N ──────────────> M equipment
```

## 4. Patient Domain

```
┌─────────────────────────────────────┐
│      PATIENT MANAGEMENT (4)         │
└─────────────────────────────────────┘
              │
         ┌────▼─────┐
         │ patients │
         │  (15)    │
         └────┬─────┘
              │ 1
              │
        ┌─────┼──────────┬─────────────┐
        │ N   │ N        │ N           │ N
        │     │          │             │
   ┌────▼──┐ ┌─▼─────┐ ┌▼──────────────┐ ┌▼──────────────┐
   │patient_│ │patient_│ │patient_       │ │patient_       │
   │addresses│ │emergency│emergency_     │ │allergies      │
   │(67)    │ │contacts │contacts       │ │(26)           │
   │        │ │(75)     │(75)           │ │               │
   └────────┘ └────────┘ └───────────────┘ └───────────────┘

Relationships:
- patients 1 ──────────────> N patient_addresses
- patients 1 ──────────────> N patient_emergency_contacts
- patients 1 ──────────────> N patient_allergies
```

## 5. Healthcare Providers Domain

```
┌─────────────────────────────────────┐
│    HEALTHCARE PROVIDERS (7)         │
└─────────────────────────────────────┘
              │
        ┌─────┼──────────┐
        │     │          │
   ┌────▼──┐ ┌▼─────┐ ┌─▼────┐
   │doctors │ │nurses │ │staff │
   │(15)   │ │(13)  │ │(8)   │
   └────┬──┘ └──┬───┘ └──┬───┘
        │       │        │
        │ N     │ N      │ N
        │       │        │
   ┌────▼───────┴────────┴────┐
   │   staff_shifts           │
   │   (126)                  │
   └──────────────────────────┘
        │
   ┌────▼─────────────┐
   │specialists       │
   │(8)               │
   └──────────────────┘
   
   ┌────────────────────┐
   │doctor_schedules    │
   │(91)                │
   │                    │
   │ 1 doctor ──> N schedules
   └────────────────────┘
   
   ┌──────────────────────────────┐
   │nurse_assignments             │
   │(13)                           │
   │                              │
   │ N nurses ──> N patients     │
   │ N nurses ──> N beds         │
   └──────────────────────────────┘

Relationships:
- departments N ──────────────> M doctors
- departments N ──────────────> M nurses
- departments N ──────────────> M staff
- doctors 1 ──────────────> N specialists
- doctors 1 ──────────────> N doctor_schedules
- nurses N ──────────────> M patients (assignments)
- nurses N ──────────────> M beds (assignments)
- staff/nurses 1 ──────────────> N staff_shifts
```

## 6. Appointments & Scheduling Domain

```
┌──────────────────────────────────┐
│ APPOINTMENTS & SCHEDULING (3)    │
└──────────────────────────────────┘
            │
      ┌─────▼──────┐
      │appointment_ │
      │types        │
      │(5)          │
      └─────┬──────┘
            │ 1:N
            │
      ┌─────▼──────────────┐
      │appointments        │
      │(5)                 │
      └─────┬──────────────┘
            │ 1:N
            │
      ┌─────▼─────────────────┐
      │appointment_           │
      │cancellations          │
      │(tracking)             │
      └───────────────────────┘

Relationships:
- appointment_types 1 ──────────────> N appointments
- appointments 1 ──────────────> N appointment_cancellations
- patients N ──────────────> M appointments
- doctors N ──────────────> M appointments
- rooms N ──────────────> M appointments
```

## 7. Clinical Encounters Domain

```
┌─────────────────────────────────────┐
│   CLINICAL ENCOUNTERS (6)           │
└─────────────────────────────────────┘
            │
        ┌───▼──────┐
        │encounters│
        │(~5)      │
        └───┬──────┘
            │ 1
            │
        ┌───┼──────────────────┬──────────┐
        │ N │ N                │ N        │ N
        │   │                  │          │
  ┌─────▼──┐ ┌──────────────┐ ┌▼────────┐ ┌▼──────────────┐
  │encounter_│ │encounter_    │ │encounter_│ │clinical_      │
  │vitals   │ │diagnoses     │ │procedures│ │notes          │
  │(~5)     │ │(~5)          │ │(~5)     │ │(~5)           │
  └─────────┘ └──────────────┘ └─────────┘ └───────────────┘
        │ N
        │
  ┌─────▼────────────┐
  │bed_assignments   │
  │(~5)              │
  └──────────────────┘

Relationships:
- patients 1 ──────────────> N encounters
- doctors N ──────────────> M encounters
- appointments N ──────────────> M encounters
- rooms N ──────────────> M encounters
- beds N ──────────────> M encounters
- encounters 1 ──────────────> N encounter_vitals
- encounters 1 ──────────────> N encounter_diagnoses
- encounters 1 ──────────────> N encounter_procedures
- encounters 1 ──────────────> N clinical_notes
- encounters 1 ──────────────> N bed_assignments
- icd_codes N ──────────────> M encounter_diagnoses
- cpt_codes N ──────────────> M encounter_procedures
```

## 8. Laboratory Services Domain

```
┌─────────────────────────────────────┐
│   LABORATORY SERVICES (5)           │
└─────────────────────────────────────┘
            │
        ┌───▼──────┐
        │lab_orders│
        │(~5)      │
        └───┬──────┘
            │ 1
            │
        ┌───▼────────┐
        │lab_tests   │
        │(~10)       │
        └───┬────────┘
            │ 1
            │
        ┌───▼──────────┐
        │lab_results   │
        │(~10)         │
        └───────────────┘

Relationships:
- patients 1 ──────────────> N lab_orders
- doctors N ──────────────> M lab_orders (ordering)
- encounters N ──────────────> M lab_orders
- lab_orders 1 ──────────────> N lab_tests
- lab_tests 1 ──────────────> N lab_results
```

## 9. Radiology Services Domain

```
┌─────────────────────────────────────┐
│   RADIOLOGY SERVICES (Integrated)   │
└─────────────────────────────────────┘
            │
        ┌───▼──────────┐
        │radiology_    │
        │orders        │
        │(~5)          │
        └───┬──────────┘
            │ 1
            │
        ┌───▼──────────┐
        │radiology_    │
        │results       │
        │(~5)          │
        └───────────────┘

Relationships:
- patients 1 ──────────────> N radiology_orders
- doctors N ──────────────> M radiology_orders (ordering)
- encounters N ──────────────> M radiology_orders
- radiology_orders 1 ──────────────> N radiology_results
- doctors N ──────────────> M radiology_results (reading)
```

## 10. Pharmacy & Medications Domain

```
┌──────────────────────────────────────────┐
│   PHARMACY & MEDICATIONS (6)             │
└──────────────────────────────────────────┘
            │
      ┌─────┴─────┐
      │           │
  ┌───▼────────┐  ┌──▼────────────┐
  │medications │  │drug_           │
  │(40+)       │  │interactions    │
  │            │  │(20)            │
  └───┬────────┘  └────────────────┘
      │
      │ 1:N
      │
  ┌───▼──────────┐
  │prescriptions │
  │(~5)          │
  └───┬──────────┘
      │ 1:N
      │
  ┌───▼──────────────┐
  │prescription_     │
  │refills          │
  │(tracking)       │
  └──────────────────┘
      
  ┌────────────────────┐
  │medication_         │
  │inventory           │
  │(~5)                │
  │                    │
  │ 1 medication ──> N inventory records
  └────────────────────┘
  
  ┌────────────────────┐
  │pharmacy_orders     │
  │(replenishment)     │
  │                    │
  │ 1 medication ──> N orders
  └────────────────────┘

Relationships:
- medications N ──────────────> M drug_interactions
- patients 1 ──────────────> N prescriptions
- doctors N ──────────────> M prescriptions
- encounters N ──────────────> M prescriptions
- medications N ──────────────> M prescriptions
- prescriptions 1 ──────────────> N prescription_refills
- medications 1 ──────────────> N medication_inventory
- medications 1 ──────────────> N pharmacy_orders
```

## 11. Insurance & Claims Domain

```
┌────────────────────────────────────────────┐
│   INSURANCE & CLAIMS (7)                   │
└────────────────────────────────────────────┘
            │
      ┌─────▼──────────┐
      │insurance_      │
      │companies       │
      │(10)            │
      └─────┬──────────┘
            │ 1:N
            │
      ┌─────▼────────┐
      │insurance_    │
      │plans         │
      │(4)           │
      └─────┬────────┘
            │ 1:N
      ┌─────▼──────────────────┐
      │patient_insurance_      │
      │policies                │
      │(3)                     │
      └─────┬──────────────────┘
            │ 1:N
      ┌─────▼─────────────┐
      │insurance_         │
      │authorizations     │
      │(pre-auth)         │
      └───────────────────┘
      
      Also:
      ┌────────────────────────┐
      │insurance_claims        │
      │(claim submissions)     │
      └────┬───────────────────┘
           │ 1:N
      ┌────▼────────────────┐
      │insurance_claim_     │
      │items                │
      │(line items)         │
      └─────────────────────┘

Relationships:
- insurance_companies 1 ──────────────> N insurance_plans
- insurance_plans 1 ──────────────> N patient_insurance_policies
- patients 1 ──────────────> N patient_insurance_policies
- patient_insurance_policies 1 ──────────────> N insurance_authorizations
- patients 1 ──────────────> N insurance_claims
- patient_insurance_policies N ──────────────> M insurance_claims
- encounters N ──────────────> M insurance_claims
- insurance_claims 1 ──────────────> N insurance_claim_items
- cpt_codes N ──────────────> M insurance_claim_items
- icd_codes N ──────────────> M insurance_claim_items
```

## 12. Billing & Payments Domain

```
┌────────────────────────────────────┐
│   BILLING & PAYMENTS (3)           │
└────────────────────────────────────┘
            │
        ┌───▼────────┐
        │invoices    │
        │(~5)        │
        └───┬────────┘
            │ 1:N
            │
      ┌─────▼──────────┐
      │invoice_items   │
      │(~10)           │
      └─────┬──────────┘
            │
            │ Also:
            │
        ┌───▼────────────────┐
        │payment_            │
        │transactions        │
        │(~5)                │
        └────────────────────┘

Relationships:
- patients 1 ──────────────> N invoices
- encounters N ──────────────> M invoices
- invoices 1 ──────────────> N invoice_items
- cpt_codes N ──────────────> M invoice_items
- invoices 1 ──────────────> N payment_transactions
- patients N ──────────────> M payment_transactions
```

## 13. System Administration Domain

```
┌───────────────────────────────────────┐
│   SYSTEM ADMINISTRATION (4)           │
└───────────────────────────────────────┘
            │
      ┌─────┴──────────┬─────────────┐
      │                │             │
  ┌───▼───┐        ┌───▼────┐   ┌───▼──────────┐
  │users  │        │roles   │   │audit_logs    │
  │(~10) │        │(~5)    │   │(comprehensive)
  └───┬───┘        └───┬────┘   └──────────────┘
      │                │
      │ N              │ N
      │                │
      └────────┬───────┘
               │
         ┌─────▼──────────┐
         │user_roles      │
         │(role mapping)  │
         └─────────────────┘

Relationships:
- users N ──────────────> M roles
- users 1 ──────────────> N audit_logs (tracking changes)
- All tables 1 ──────────────> N audit_logs
```

## 14. Complete Patient Data Flow

```
Patient Registration
       │
       ▼
    patients ──────────────────────┐
       │                           │
       ├─> patient_addresses       │
       ├─> patient_emergency_contacts
       ├─> patient_allergies       │
       └─> patient_insurance_policies
                                   │
       ┌───────────────────────────┘
       │
       ▼
  appointments ◄─────── appointment_types
       │
       ├──> appointment_cancellations
       │
       ▼
   encounters ◄──────── encounters.appointment_id
       │
       ├─> encounter_vitals
       ├─> encounter_diagnoses ◄─── icd_codes
       ├─> encounter_procedures ◄─── cpt_codes
       ├─> clinical_notes
       ├─> bed_assignments
       │
       ├─> lab_orders ─> lab_tests ─> lab_results
       ├─> radiology_orders ─> radiology_results
       ├─> prescriptions ─> prescription_refills ◄─── medications
       │
       ├─> insurance_claims ─> insurance_claim_items
       │
       └─> invoices ─> invoice_items ─> payment_transactions
```

## 15. Complete Provider Data Flow

```
departments
    │
    ├─> doctors ◄─── doctor_schedules
    │       │
    │       ├─> specialists
    │       ├─> appointments
    │       ├─> encounters
    │       ├─> lab_orders
    │       ├─> radiology_orders
    │       └─> prescriptions
    │
    ├─> nurses ◄─── nurse_assignments
    │       │        (patient assignments)
    │       └─> staff_shifts
    │
    └─> staff ◄─── staff_shifts
            └─> department_equipment
```

## 16. Key Cardinality Rules

### One-to-Many (1:N)
- `facilities 1:N rooms`
- `rooms 1:N beds`
- `departments 1:N doctors`
- `departments 1:N nurses`
- `departments 1:N staff`
- `patients 1:N addresses`
- `patients 1:N encounters`
- `patients 1:N appointments`
- `appointments 1:N cancellations`
- `encounters 1:N vitals`
- `encounters 1:N diagnoses`
- `prescriptions 1:N refills`
- `invoices 1:N items`
- `lab_orders 1:N tests`
- `insurance_companies 1:N plans`

### Many-to-Many (N:M)
- `departments N:M equipment` (via department_equipment)
- `nurses N:M patients` (via nurse_assignments)
- `medications N:M drug_interactions`
- `doctors N:M prescriptions`
- `appointments N:M clinicians`

## 17. Referential Integrity Summary

**Total Foreign Key Constraints: 82**

- **Reference Domain:** 0 (standalone)
- **Organizational Domain:** 6
- **Patient Domain:** 4
- **Provider Domain:** 12
- **Appointments Domain:** 6
- **Clinical Domain:** 18
- **Laboratory Domain:** 6
- **Pharmacy Domain:** 10
- **Insurance Domain:** 12
- **Billing Domain:** 6
- **System Admin Domain:** 4

## 18. Index Strategy

**All Foreign Keys Indexed** (82 indexes)  
**Primary Keys** (52 indexes)  
**Business Key Indexes:**
- patients.mrn
- patients.ssn
- doctors.npi_number
- doctors.license_number
- medications.ndc_code
- appointments.appointment_number
- encounters.encounter_number

**Composite Indexes:**
- (patient_id, encounter_id)
- (doctor_id, appointment_date)
- (facility_id, room_number)

---

**Last Updated:** February 2026  
**Total Domains:** 11  
**Total Tables:** 52  
**Total FK Relationships:** 82  
**Total Views:** 15  
**Status:** Production-Ready (Prompt 25)
