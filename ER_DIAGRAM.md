# Hospital OLTP System - Entity Relationship Diagram

This document provides visual representations of the database schema relationships.

## High-Level Domain Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOSPITAL OLTP SYSTEM                         │
│                      ~50 Tables Total                           │
└─────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
    ┌───▼────┐                                   ┌────▼───┐
    │PATIENTS│                                   │PROVIDERS│
    │Domain  │                                   │ Domain │
    └───┬────┘                                   └────┬───┘
        │                                             │
        ├─patients (4)                               ├─doctors (8)
        ├─patient_addresses                          ├─nurses
        ├─patient_emergency_contacts                 ├─staff
        └─patient_allergies                          ├─specialists
                                                     ├─doctor_schedules
        ┌────────────────┐                          ├─staff_shifts
        │                │                          ├─nurse_assignments
    ┌───▼────┐      ┌────▼───┐                    └─ (relationships)
    │CLINICAL│      │FACILITY│
    │Domain  │      │ Domain │                    ┌────────────┐
    └───┬────┘      └────┬───┘                    │ REFERENCE  │
        │                │                        │   DATA     │
        ├─encounters (6)  ├─facilities (6)        └────┬───────┘
        ├─encounter_vitals                             │
        ├─encounter_diagnoses                          ├─icd_codes (2)
        ├─encounter_procedures                         └─cpt_codes
        ├─clinical_notes
        └─bed_assignments   ├─departments
                           ├─facilities
        ┌────────────────┐ ├─rooms
        │                │ ├─beds
    ┌───▼────┐      ┌────▼───┐ └─equipment
    │ LAB &  │      │PHARMACY│
    │RADIOLOGY│      │ Domain │                   ┌────────────┐
    └───┬────┘      └────┬───┘                   │ INSURANCE  │
        │                │                        │ & BILLING  │
        ├─lab_orders (5)  ├─medications (6)       └────┬───────┘
        ├─lab_tests       ├─drug_interactions           │
        ├─lab_results     ├─prescriptions              ├─insurance_companies (7)
        ├─radiology_orders├─prescription_refills       ├─insurance_plans
        └─radiology_results                            ├─patient_insurance_policies
                           ├─medication_inventory      ├─insurance_authorizations
    ┌──────────────────┐ └─pharmacy_orders            ├─insurance_claims
    │  APPOINTMENTS    │                              └─insurance_claim_items
    │   & SCHEDULING   │
    └────┬─────────────┘                             ┌────────────┐
         │                                           │   BILLING  │
         ├─appointment_types (3)                     └────┬───────┘
         ├─appointments                                   │
         └─appointment_cancellations                     ├─invoices (3)
                                                         ├─invoice_items
                                                         └─payment_transactions
    ┌──────────────────┐
    │     SYSTEM       │
    │ ADMINISTRATION   │
    └────┬─────────────┘
         │
         ├─users (4)
         ├─roles
         ├─user_roles
         └─audit_logs
```

## Core Relationships Map

### Patient-Centric Flow
```
                         ┌─────────────┐
                         │  PATIENTS   │
                         │  (Core)     │
                         └──────┬──────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼───────┐  ┌───▼─────┐  ┌──────▼────────┐
        │patient_       │  │patient_ │  │patient_       │
        │addresses      │  │emergency│  │allergies      │
        └───────────────┘  │_contacts│  └───────────────┘
                           └─────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼────┐   ┌──────▼────┐   ┌─────▼──────┐
        │appointments│   │patient_   │   │insurance   │
        │            │   │insurance_ │   │_claims     │
        └─────┬──────┘   │policies   │   └─────┬──────┘
              │          └─────┬─────┘         │
              │                │               │
        ┌─────▼──────┐   ┌─────▼──────┐  ┌────▼───────┐
        │encounters  │   │insurance_  │  │claim_items │
        │            │   │claims      │  └────────────┘
        └─────┬──────┘   └────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼───┐ ┌───▼────┐
│vitals │ │diag- │ │proce-  │
│       │ │noses │ │dures   │
└───────┘ └──────┘ └────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼──────┐ ┌▼────┐ ┌─▼──────┐
│lab_orders│ │Rx   │ │invoices│
└────┬─────┘ └┬────┘ └───┬────┘
     │        │           │
┌────▼────┐ ┌▼──────┐ ┌──▼─────┐
│lab_tests│ │refills│ │invoice │
└────┬────┘ └───────┘ │_items  │
     │                └───┬────┘
┌────▼───────┐           │
│lab_results │      ┌────▼────────┐
└────────────┘      │payment_     │
                    │transactions │
                    └─────────────┘
```

### Provider Management Flow
```
┌──────────────┐
│ DEPARTMENTS  │
└──────┬───────┘
       │
   ┌───┴───────────┬──────────────┐
   │               │              │
┌──▼──────┐   ┌────▼───┐    ┌────▼────┐
│ DOCTORS │   │ NURSES │    │  STAFF  │
└────┬────┘   └────┬───┘    └────┬────┘
     │             │              │
     ├─specialists │              │
     ├─schedules   ├─assignments  ├─shifts
     │             │              │
     └─────────────┴──────────────┘
                   │
            ┌──────┴──────┐
            │             │
     ┌──────▼────┐  ┌─────▼────┐
     │appointments│ │encounters│
     └────────────┘ └──────────┘
```

### Facility & Bed Management
```
┌───────────┐
│FACILITIES │
└─────┬─────┘
      │
  ┌───▼────┐
  │ ROOMS  │──────┐
  └───┬────┘      │
      │           │
  ┌───▼───┐   ┌───▼────────┐
  │ BEDS  │   │appointments│
  └───┬───┘   └────────────┘
      │
  ┌───▼───────────┐
  │bed_assignments│
  └───────────────┘
```

### Diagnostic Workflow
```
┌───────────┐
│ENCOUNTERS │
└─────┬─────┘
      │
 ┌────┴────────┐
 │             │
┌▼──────────┐ ┌▼────────────┐
│LAB_ORDERS │ │RADIOLOGY_   │
│           │ │ORDERS       │
└─────┬─────┘ └──────┬──────┘
      │              │
┌─────▼──────┐  ┌────▼─────────┐
│ LAB_TESTS  │  │RADIOLOGY_    │
└─────┬──────┘  │RESULTS       │
      │         └──────────────┘
┌─────▼──────┐
│LAB_RESULTS │
└────────────┘
```

### Medication Management
```
┌──────────────┐
│ MEDICATIONS  │
└──────┬───────┘
       │
  ┌────┴──────────┬────────────┐
  │               │            │
┌─▼────────────┐ ┌▼──────────┐ ┌▼────────────┐
│drug_         │ │medication_│ │prescriptions│
│interactions  │ │inventory  │ └──────┬──────┘
└──────────────┘ └─────┬─────┘        │
                       │         ┌────▼────────┐
                  ┌────▼──────┐  │prescription_│
                  │pharmacy_  │  │refills      │
                  │orders     │  └─────────────┘
                  └───────────┘
```

### Insurance & Claims Processing
```
┌──────────────────┐
│INSURANCE_        │
│COMPANIES         │
└────────┬─────────┘
         │
    ┌────▼────────┐
    │INSURANCE_   │
    │PLANS        │
    └────┬────────┘
         │
    ┌────▼───────────────┐
    │PATIENT_INSURANCE_  │
    │POLICIES            │
    └────┬───────────────┘
         │
    ┌────┴─────────┬──────────────┐
    │              │              │
┌───▼──────────┐ ┌▼────────────┐ ┌▼──────────┐
│INSURANCE_    │ │INSURANCE_   │ │INSURANCE_ │
│AUTHORIZATIONS│ │CLAIMS       │ │CLAIMS     │
└──────────────┘ └──────┬──────┘ └───────────┘
                        │
                  ┌─────▼────────┐
                  │CLAIM_ITEMS   │
                  └──────────────┘
```

### Billing & Payments
```
┌────────────┐
│ ENCOUNTERS │
└──────┬─────┘
       │
  ┌────▼────────┐
  │  INVOICES   │
  └──────┬──────┘
         │
    ┌────┴──────┬────────────────┐
    │           │                │
┌───▼────────┐ ┌▼──────────┐ ┌──▼─────────────┐
│INVOICE_    │ │INSURANCE_  │ │PAYMENT_        │
│ITEMS       │ │CLAIMS      │ │TRANSACTIONS    │
└────────────┘ └────────────┘ └────────────────┘
```

## Key Cardinality Relationships

### One-to-Many (1:N)
- **patients** → patient_addresses (1 patient : many addresses)
- **patients** → appointments (1 patient : many appointments)
- **doctors** → appointments (1 doctor : many appointments)
- **departments** → doctors (1 department : many doctors)
- **encounters** → encounter_vitals (1 encounter : many vital readings)
- **medications** → prescriptions (1 medication : many prescriptions)

### Many-to-Many (M:N) via Junction Tables
- **medications** ↔ **medications** via drug_interactions
- **users** ↔ **roles** via user_roles
- **departments** ↔ **equipment** via department_equipment

### Self-Referencing
- **appointments** → parent_appointment_id (follow-up appointments)
- **prescriptions** → original_prescription_id (refill tracking)

## Foreign Key Cascade Behaviors

### ON DELETE CASCADE
Used for dependent data that should be removed with parent:
- patient_addresses when patient deleted
- appointments when patient/doctor deleted
- encounter_vitals when encounter deleted
- lab_tests when lab_order deleted

### ON DELETE SET NULL
Used for optional references:
- doctor.department_id (doctor can exist without department assignment)
- appointment.room_id (appointment can exist without room)
- encounter.appointment_id (encounter may not be from appointment)

### ON DELETE RESTRICT
Used for reference data that must not be deleted if referenced:
- icd_codes (cannot delete if used in diagnoses)
- cpt_codes (cannot delete if used in procedures)
- medications (cannot delete if prescribed)

## Database Normalization

### Normal Forms Achieved
- **1NF**: All tables have atomic values, no repeating groups
- **2NF**: All non-key attributes fully dependent on primary key
- **3NF**: No transitive dependencies
- **BCNF**: Most tables in Boyce-Codd Normal Form

### Denormalization for Performance
- Computed columns: amount_due in invoices, age calculation
- Summary views for reporting
- Redundant foreign keys for direct access (e.g., prescriptions has both encounter_id and patient_id)

## Indexing Strategy Summary

### Primary Indexes
- All tables have PRIMARY KEY with AUTO_INCREMENT
- Natural keys have UNIQUE constraints

### Secondary Indexes
- All foreign keys indexed
- Frequently searched fields (mrn, npi_number, dates)
- Status fields for filtering
- Composite indexes on name fields

### Full-Text Indexes (Optional Enhancement)
- clinical_notes.note_text
- encounter_diagnoses.diagnosis_description
- radiology_results.findings

---

*For detailed table definitions, see SCHEMA_DOCUMENTATION.md*
*For SQL implementation, see create_schema.sql*
