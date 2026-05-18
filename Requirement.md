# Requirement Specification — Small Hospital Front-End Tool

**Project:** DTP Hospital OLTP System — Front-End Application
**Source Document:** `Design Analysis and Recommendations for Small Hospital Front.docx`
**Backend:** Existing MySQL OLTP database (`hospital_OLTP_system`) — 52 tables, 82 FK relationships, 15 reporting views, 11 domains
**Target Audience:** Small hospitals (lighter alternative to Epic Clarity)
**Document Date:** 2026-05-16
**Status:** Draft v1.0

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Human-Readable Prompt (Business Narrative)](#2-human-readable-prompt-business-narrative)
3. [Detailed Technical Prompt (Engineering Specification)](#3-detailed-technical-prompt-engineering-specification)
4. [Functional Modules](#4-functional-modules)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Domain & Database Mapping](#6-domain--database-mapping)
7. [Security & Compliance](#7-security--compliance)
8. [UI / UX Requirements](#8-ui--ux-requirements)
9. [Integration Points](#9-integration-points)
10. [Acceptance Criteria](#10-acceptance-criteria)
11. [Out of Scope (v1)](#11-out-of-scope-v1)
12. [Glossary](#12-glossary)

---

## 1. Executive Summary

### 1.1 Vision

Build a **lightweight Hospital Management System (HMS)** for small hospitals — a slimmed-down equivalent of **Epic Clarity** — that captures essential clinical and administrative data electronically. The system must let hospital staff **access, manage, and analyze data efficiently** to support both clinical decision-making and day-to-day administration.

The product philosophy is explicit: deliver **80% of Epic's workflow value at 20% of its complexity, cost, and onboarding burden**. We are not building an enterprise EHR. We are building the smallest tool a 25-to-100-bed community hospital actually needs to run patient flow, clinical documentation, pharmacy, billing, and management reporting from a single, audited, role-controlled web application.

### 1.2 Context & Problem Statement

#### 1.2.1 Why Now
Small hospitals are under three converging pressures:

1. **Cost pressure** — enterprise EHRs (Epic, Cerner) carry license, hardware, and implementation costs that exceed the operating budget of a typical small/rural hospital.
2. **Compliance pressure** — HIPAA audit-readiness, e-prescribing, and structured ICD-10/CPT coding are increasingly non-negotiable, even for small providers.
3. **Workforce pressure** — small hospitals have lean staff who context-switch across roles (a nurse may also do intake; an admin may also do billing). The tool must serve that reality without forcing a 12-week training program.

#### 1.2.2 What Exists Today

A production-ready MySQL **OLTP backend** has already been built, validated, and seeded:

| Asset | Status |
|---|---|
| Database schema (`create_schema.sql`) | **52 tables across 11 domains, 82 FK constraints** — production-ready |
| Reporting views (`database_views.sql`) | **15 views** spanning clinical, operational, financial reporting |
| Python connection layer (`database_connection.py`) | Context-managed `DatabaseConnection` class, parameterized queries, logging |
| Initialization script (`init_database_Setup.py`) | Idempotent DB+schema+sample-data setup with timestamped logs |
| Test data loader (`load_all_fake_data.py`) | 5-layer dependency-aware loader producing **500+ records** |
| Documentation | `README.md`, `SCHEMA_DOCUMENTATION.md`, `ER_DIAGRAM.md`, `CLAUDE.md` |
| Audit framework | `audit_logs` table with old/new JSON, IP, user-agent — HIPAA-ready |
| RBAC framework | `users`, `roles`, `user_roles` tables with JSON permissions — wired but unused |

#### 1.2.3 The Gap

**There is no user interface.** Today, every interaction with the database is via raw SQL or Python scripts. This makes the system unusable by clinicians, billers, pharmacists, or administrators — the very people it was designed to serve. The 15 reporting views are valuable but invisible.

This requirements document specifies the **front-end application and supporting API tier** needed to close that gap and deliver clinical value to a real hospital.

### 1.3 Goal & Scope

#### 1.3.1 Primary Goal
Design and build a **role-based, responsive, audited web application** that exposes the existing OLTP backend through six clinically-meaningful workflows:

1. **Appointment Scheduling** — book, reschedule, cancel, remind
2. **Electronic Medical Records (EMR)** — chart, vitals, diagnoses, procedures, notes
3. **Billing & Payments** — invoices, claims, payment capture, A/R follow-up
4. **Inventory Management** — medications, lab supplies, equipment, expiry/restock
5. **Staff Management** — directory, schedules, shifts, credentials
6. **Reporting & Analytics** — surface the 15 existing views + exportable reports

#### 1.3.2 In Scope (v1)
- Responsive web UI for desktop (≥1280 px) and tablet (≥768 px)
- REST API + RBAC + audit middleware
- All six modules above, end-to-end, on the existing schema
- Reproducible local-dev environment using the existing init scripts

#### 1.3.3 Out of Scope (v1)
- Native mobile apps, HL7/FHIR, PACS image viewing, telehealth, patient portal, ML/analytics, multi-tenant, multi-language. See §11 for the full list.

### 1.4 Stakeholders

| Stakeholder | Role in System | Primary Workflows |
|---|---|---|
| **Receptionist / Front Desk** | Patient registration, appointment booking, check-in | Patients, Appointments |
| **Doctor / Provider** | Clinical documentation, orders, prescriptions | EMR, Labs, Pharmacy |
| **Nurse** | Vitals, bed assignments, nursing notes, patient education | EMR (limited write) |
| **Pharmacist** | Dispense prescriptions, inventory, restock orders | Pharmacy, Inventory |
| **Billing / Coding Staff** | Invoice generation, insurance claims, payment posting | Billing, Insurance |
| **Department Manager** | Staffing, scheduling, equipment, departmental reports | Staff, Reporting |
| **Hospital Administrator** | User management, audit review, executive dashboards | Admin, Reporting |
| **Patient** (indirect) | Subject of records; not a system user in v1 | — (future portal) |
| **Compliance / Privacy Officer** | Audit log review, access policy enforcement | Audit, RBAC |
| **IT / DBA** | Deployment, backups, monitoring, migrations | Operations |

### 1.5 Success Metrics

The v1 release is considered successful when the following measurable outcomes hold:

#### 1.5.1 Workflow Metrics
| Metric | Target |
|---|---|
| End-to-end patient visit (register → discharge → invoice) by one trained user | ≤ 10 minutes |
| Time to book an appointment | ≤ 30 seconds (after patient lookup) |
| Time to record an encounter's vitals + primary diagnosis | ≤ 90 seconds |
| Time to generate and post an invoice from a completed encounter | ≤ 60 seconds |
| New-user productive proficiency | ≤ 2 hours of guided training |

#### 1.5.2 Technical Metrics
| Metric | Target |
|---|---|
| p95 read latency | < 300 ms |
| p95 write latency | < 800 ms |
| Dashboard render (500+ rows) | < 1.5 s |
| Concurrent users supported | ≥ 50 |
| Uptime (business hours) | ≥ 99.5% |
| RPO (data loss tolerance) | ≤ 24 h |
| RTO (recovery time) | ≤ 4 h |

#### 1.5.3 Quality Metrics
| Metric | Target |
|---|---|
| Backend unit test coverage | ≥ 80% |
| Critical workflow e2e tests | 100% of the 8 acceptance workflows in §10 |
| HIPAA audit-trail completeness | 100% of PHI mutations logged |
| Accessibility | WCAG 2.1 AA on all 15 screens |
| Open high/critical security findings (bandit, ZAP) | 0 at release |

### 1.6 Key Business Drivers

The features called out in `Design Analysis and Recommendations for Small Hospital Front.docx` map to these concrete drivers:

| Driver | Module(s) | Why it matters to a small hospital |
|---|---|---|
| Reduce missed appointments | Appointment Scheduling + reminders | Each no-show is direct lost revenue; reminders cut no-shows ~30%. |
| Eliminate paper charts | EMR | Faster chart access, fewer transcription errors, audit-ready. |
| Accelerate cash collection | Billing & Payments | Days-in-A/R directly affects working capital. |
| Prevent stockouts and expiry waste | Inventory | Pharmacy is a top-3 cost center; expiry waste is avoidable. |
| Optimize staff utilization | Staff Management | Lean staffing means schedule mistakes are immediately painful. |
| Enable data-driven decisions | Reporting | Leadership today has no live operational visibility. |
| HIPAA audit readiness | RBAC + Audit Logs | A single compliance failure can close a small hospital. |

### 1.7 Guiding Principles

1. **Schema is authoritative.** The 52-table OLTP schema is the source of truth. The application bends to it, not the other way around.
2. **Reuse what exists.** `database_connection.py`, the 15 views, `audit_logs`, the RBAC tables, the init scripts — all stay, all extend.
3. **Server-enforced security.** Every authorization check happens on the API. The client is treated as untrusted.
4. **No silent failures.** Every constraint violation surfaces as a clear, actionable user message; nothing is masked with `NULL` or `try/except: pass`.
5. **Small-team operable.** A single ops person must be able to deploy, back up, and restore the system. No Kubernetes-class complexity in v1.
6. **Workflow over forms.** Optimize the screens for the actual clinical sequence (register → schedule → encounter → orders → discharge → bill), not for raw table CRUD.
7. **Boring tech.** Established frameworks (FastAPI, React, MySQL) over novel ones. Hospitals are not the place to try the new thing.

### 1.8 Top Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Schema drift between front-end models and the 52-table DDL | Medium | High | Generate Pydantic + Zod from a single OpenAPI; CI test recreates DB from `create_schema.sql` |
| RBAC enforced only on the client (escape hatch) | Medium | Critical (HIPAA) | All permission checks server-side; pen-test before release |
| Slow dashboards on large views | Medium | Medium | Add covering indexes; cache view results 60 s; paginate |
| Clinician resistance to electronic documentation | High | High | Co-design encounter screen with a real clinician; keyboard shortcuts; minimum mandatory fields |
| Audit log explosion | Medium | Medium | Archive `audit_logs` weekly; compress JSON; cursor pagination |
| Backup-restore drift | Low | Critical | Quarterly restore drill from `mysqldump` |
| Scope creep (HL7, PACS, patient portal in v1) | High | High | Explicit out-of-scope list (§11); change-control gate |
| Underestimating integration with insurance payers | Medium | Medium | v1 treats claims as internal-only records; real payer EDI deferred to v2 |

### 1.9 Release Strategy

| Release | Scope | Target |
|---|---|---|
| **v0.1 — Internal Alpha** | Auth + Patient CRUD + Appointment scheduling + Reports (read-only) | Internal demo |
| **v0.5 — Beta** | Full EMR + Pharmacy + Inventory + Billing on a single pilot department | Pilot department, real workflows, synthetic data |
| **v1.0 — Production** | All 6 modules, RBAC, audit, full reports, all 15 screens | One real small hospital, real PHI, with go-live support |
| **v1.x — Hardening** | Performance tuning, accessibility audit, security pen-test fixes | Same hospital |
| **v2 (future)** | HL7/FHIR, patient portal, payer EDI, mobile, multi-tenant | Out of scope here |

### 1.10 Competitive Landscape & Positioning

The product positioning is **a focused, opinionated, small-hospital tool** — not a competitor to enterprise EHRs and not a clone of open-source projects.

| System | Type | Strength | Weakness for our target | Our positioning |
|---|---|---|---|---|
| **Epic** (Clarity) | Enterprise EHR | Most comprehensive workflow coverage; deep payer integrations | License + implementation cost can exceed $1M; 9–24 month rollouts; over-built for <100-bed hospitals | We pick the 20% of Epic workflows that map to small-hospital reality. |
| **Cerner / Oracle Health** | Enterprise EHR | Strong inpatient workflows; large installed base | Similar cost/complexity profile to Epic | Same as above. |
| **athenahealth** | Cloud EHR + RCM | SaaS, strong revenue-cycle management | Per-provider monthly fees add up; opinionated workflow forces process change | We give the hospital ownership of its data and schema. |
| **OpenEMR** | Open-source EHR | Free; broad community | UI dated, accessibility gaps, sprawling configuration, security posture varies by deployer | We offer a modern UX, opinionated security defaults, and auditability out of the box. |
| **OpenMRS** | Open-source EHR (global health) | Strong for low-resource settings | Java/OSGi complexity; not US-billing-oriented | We are US-coded (ICD-10, CPT, NDC, NPI) from day one. |
| **Practice Fusion / DrChrono** | Ambulatory EHR | Fast for outpatient clinics | Limited inpatient/bed/ICU support | We cover inpatient stays, beds, and ICU. |
| **Our product** | Custom HMS on owned schema | Owned data; modern UX; opinionated security; small-hospital scope | Smaller feature surface than enterprise systems | "Epic Clarity for a 50-bed hospital, without the Epic price tag or 18-month rollout." |

**One-sentence positioning:** *"A self-hostable, schema-owned, audit-ready hospital management web app, designed specifically for small hospitals that want Epic-class workflow discipline without Epic-class cost or complexity."*

### 1.11 Regulatory & Compliance Landscape

The system must operate inside a US healthcare regulatory frame. The v1 scope is HIPAA-ready and audit-trail complete; deeper certifications are deferred to v2 but must not be designed-out.

| Regulation / Standard | Applicability | v1 Stance | v2+ Roadmap |
|---|---|---|---|
| **HIPAA Privacy Rule** | All PHI handling | **Required** — minimum-necessary access, RBAC, audit logging, SSN masking, PHI not in URLs/logs | Formal BAAs, signed authorizations workflow |
| **HIPAA Security Rule** | All electronic PHI | **Required** — TLS 1.2+, encryption at rest, account lockout, session timeout | Hardware MFA, formal risk analysis |
| **HITECH Act** | Breach notification, audit | **Required** — audit logs immutable, retention ≥ 6 years | Automated breach detection |
| **21st Century Cures Act (Info Blocking)** | Patient data portability | Out of scope v1 | Patient portal + FHIR export in v2 |
| **ICD-10-CM / ICD-10-PCS** | Diagnosis coding | **Required** — `icd_codes` is FK-enforced on diagnoses | Quarterly code updates automated |
| **CPT (AMA) / HCPCS** | Procedure/billing coding | **Required** — `cpt_codes` FK-enforced | Automated annual license sync |
| **NPI (CMS)** | Provider identification | **Required** — `doctors.npi_number` unique | NPI registry validation |
| **NDC (FDA)** | Medication identification | **Required** — `medications.ndc_code` | RxNorm cross-walk |
| **DEA Schedule** | Controlled substances | **Required** — `medications.dea_schedule` field; flagged in UI | Full e-prescribing of controlled substances (EPCS) |
| **ONC Certification (Health IT)** | Meaningful Use / Promoting Interoperability | Out of scope v1 | v2 candidate if customers request MIPS reporting |
| **State medical board licensing** | Provider license validity | **Required** — `doctors.license_expiry` field with UI warnings | Automated license registry checks |
| **PCI-DSS** | Card payment data | Out of scope v1 — card numbers never stored | Hosted-checkout integration in v2 |
| **WCAG 2.1 AA** | Accessibility | **Required** for all v1 screens | WCAG 2.2 AAA on critical paths |
| **GDPR / state privacy laws (CCPA, etc.)** | Patient data subject rights | Out of scope v1 (US-only) | Right-to-erasure workflow if needed |

### 1.12 Assumptions

The plan and effort estimates rest on the following explicit assumptions. If any flips, the plan must be re-baselined.

1. The **existing MySQL schema is stable** and will not change shape during v1 build except via additive migrations.
2. The hospital provides **a single MySQL instance** (managed or self-hosted) accessible from the API tier.
3. **Network connectivity** at the hospital is reliable enough for a browser-based app; offline-first is not required in v1.
4. The hospital has **at least one IT-capable contact** for deployment, backups, and user provisioning.
5. **English-only UI** is acceptable for v1.
6. **No real-time integration with payers** in v1 — claims are recorded internally and exported as files if needed.
7. **No real-time integration with lab analyzers or PACS** — results are entered manually or imported in batch.
8. **One hospital per deployment** — multi-tenant is deferred to v2.
9. The **15 existing database views** are correct and performant; they remain the canonical reporting surface.
10. The team has **at least one clinical SME** available to validate workflows before pilot.

### 1.13 Dependencies

| Dependency | Owner | Needed by | Risk if late |
|---|---|---|---|
| MySQL 8.0+ instance with `hospital_OLTP_system` initialized | Hospital IT / DBA | Alpha (v0.1) | Cannot start backend development |
| TLS certificate (Let's Encrypt or hospital CA) | Hospital IT | Beta (v0.5) | Cannot expose pilot to real users |
| Authoritative ICD-10 and CPT code seed data | Coding / Compliance | Alpha | Diagnoses/procedures cannot be entered |
| Clinical SME availability (≥ 4 hrs/week) | Hospital | Throughout | Workflow screens get redesigned post-pilot — expensive |
| User identity list (who maps to which role) | Hospital admin | Pre-Beta | Cannot seed `users` / `user_roles` |
| Backup storage location + access | Hospital IT | Pre-Production | No DR posture |
| Hosting target decided (on-prem vs cloud VM vs managed) | Hospital + IT | Pre-Production | Deployment scripts diverge late |
| Security pen-test window | External vendor or in-house | Before v1.0 | Cannot certify go-live readiness |
| Training time with end-users (≥ 2 hrs / user) | Hospital ops | At go-live | Adoption stalls |

### 1.14 High-Level Timeline & Milestones

Indicative — actuals depend on team size and SME availability. Assumes one full-time backend engineer, one full-time frontend engineer, and a part-time clinical SME.

| Phase | Duration | Milestone | Deliverable |
|---|---|---|---|
| **0. Discovery & Setup** | 2 wks | M0: Repo + CI + env ready | Backend skeleton, Docker Compose, OpenAPI scaffold, frontend Vite scaffold |
| **1. Foundations** | 3 wks | M1: Auth + RBAC + audit middleware working | Login flow, JWT, audit logs verified, 1 sample CRUD endpoint |
| **2. Patient & Appointment** | 3 wks | M2: Internal Alpha (v0.1) | Patient registration, appointments, today's view, reports list |
| **3. EMR Core** | 4 wks | M3: Encounters end-to-end | Vitals, diagnoses, procedures, clinical notes, ICD/CPT lookups |
| **4. Pharmacy & Labs** | 3 wks | M4: Lab + Rx pipeline | Lab orders → results, prescriptions, inventory decrements |
| **5. Billing & Insurance** | 3 wks | M5: Beta (v0.5) | Invoices, claims, payments, A/R aging, pilot-department demo |
| **6. Inventory & Staff Admin** | 2 wks | M6: All 6 modules feature-complete | Low-stock alerts, doctor schedules, staff directory |
| **7. Reporting & Polish** | 2 wks | M7: All 15 reports surfaced | Dashboard tiles, exports (CSV/PDF), accessibility pass |
| **8. Hardening** | 3 wks | M8: Pen-test passed | Performance tuning, security fixes, WCAG audit, DR drill |
| **9. Pilot** | 4 wks | M9: Production (v1.0) at one hospital | Go-live support, runbook, training, on-call rotation |
| **Total** | **~29 wks (~7 months)** | | |

### 1.15 Cost Categories (Indicative)

This is a structural breakdown, not a price quote. Actual numbers depend on hosting choices, team rates, and pilot scope.

| Category | One-time | Recurring (annual) | Notes |
|---|---|---|---|
| **Engineering build** (backend + frontend + QA) | ✓ | — | The bulk of v1 cost; ~7 months effort per §1.14 |
| **Clinical SME time** | ✓ | — | ≥ 4 hrs/week throughout build |
| **Security pen-test + remediation** | ✓ | ✓ (annual retest) | Required before v1.0 |
| **Hosting** (cloud VMs or on-prem hardware) | small | ✓ | One API host, one DB host, one bastion / backup |
| **Managed MySQL** (if chosen) | — | ✓ | Trade-off vs self-hosted |
| **TLS certs** | — | ✓ (free if Let's Encrypt) | Renewals automated |
| **Backups & DR storage** | — | ✓ | Encrypted offsite |
| **Code licenses** (AMA CPT) | ✓ | ✓ (annual) | CPT codes are licensed by the AMA |
| **Training** (initial + ongoing) | ✓ | small | Per-user, on-site or recorded |
| **Support / on-call** | — | ✓ | Especially first 90 days post go-live |
| **Future v2 items** | deferred | deferred | HL7/FHIR, portal, mobile, multi-tenant |

### 1.16 Key Architectural Decisions (Decision Log)

These are decisions already taken in this requirements document. Each is recorded with its rationale so future contributors can challenge or rely on it.

| # | Decision | Alternatives considered | Rationale |
|---|---|---|---|
| AD-01 | Build on the existing 52-table MySQL OLTP schema as-is | Greenfield schema; PostgreSQL port | Schema is production-ready, FK-complete, and reflects real hospital domains. |
| AD-02 | FastAPI (Python) for backend | Flask, Django, Node/Express, Go | Async, auto-OpenAPI, plays well with existing `database_connection.py`. |
| AD-03 | Raw SQL + Pydantic over ORM | SQLAlchemy ORM, Tortoise | Schema with 82 FKs and generated columns is friction-heavy for ORMs. |
| AD-04 | React + TypeScript + Vite | Vue, Angular, Svelte | Largest ecosystem, type-safety, smallest hiring risk. |
| AD-05 | JWT + httpOnly refresh cookies | Server-session, OAuth | Stateless API; refresh in cookie reduces XSS risk. |
| AD-06 | RBAC enforced server-side via decorators | Casbin / OPA, client-side only | Simple, audit-friendly, sufficient for v1 role count. |
| AD-07 | Audit log written inside the same transaction as the mutation | Async event stream | Strong consistency; no risk of "mutation logged, change rolled back" divergence. |
| AD-08 | Surface the 15 existing views as `/api/v1/reports/{view}` | Re-query in code | Views are already tuned and indexed. |
| AD-09 | Desktop + tablet only in v1 | Mobile-first | Real clinical use happens on workstations and tablets; phones come later. |
| AD-10 | English-only UI in v1 | i18n from day one | Schema reserves `preferred_language`; defer the UI cost until needed. |
| AD-11 | One hospital per deployment | Multi-tenant from v1 | Multi-tenant adds significant complexity (row-level security, tenant isolation) for zero v1 value. |
| AD-12 | No real-time payer EDI in v1 | Full X12 integration | Each payer integration is a project; defer to v2 with explicit per-payer scope. |
| AD-13 | Manual lab result entry in v1 | Analyzer interface (HL7) | Pilot hospital can be without an analyzer interface; HL7 is v2. |
| AD-14 | APScheduler for jobs in v1; Celery/Redis only if scaled | Celery from day one | Avoid unnecessary infrastructure for a small-hospital workload. |

### 1.17 Operating Model (Post Go-Live)

The system must be operable by a small team. The day-to-day operating model:

| Responsibility | Who | Cadence |
|---|---|---|
| User provisioning (add/remove staff accounts) | Hospital admin | Ad hoc |
| Role assignment | Hospital admin (with compliance sign-off) | Ad hoc |
| Audit log review | Compliance officer | Weekly |
| Backup verification (restore from yesterday's dump) | Hospital IT | Weekly |
| Patch + dependency updates (security only) | Vendor / build team | Monthly |
| Feature releases | Vendor / build team | Quarterly |
| Full DR drill (restore to a clean host) | Hospital IT + vendor | Quarterly |
| Penetration test | External vendor | Annually |
| License renewals (CPT, TLS) | Hospital IT | Annually |
| ICD-10 code refresh | Compliance / Coding | Annually |

**Support model:** named on-call engineer for first 90 days post go-live; business-hours support thereafter; runbook covers the top 10 incidents (login failure, slow report, FK error, backup failure, certificate expiry, etc.).

### 1.18 Change Management & Adoption Plan

A small hospital adopts new clinical software with difficulty. The plan must include people work, not just technical work.

| Audience | Intervention | When |
|---|---|---|
| **Clinical leadership** (medical director, nursing director) | 1-hour walkthrough, success-metric review, escalation channel | Pre-pilot and at each milestone |
| **Pilot department staff** | 2-hour on-site training; printed quick-reference cards; instructor on-site for first 3 days | Beta (v0.5) |
| **All staff** | Recorded role-specific videos (8–12 min each); written FAQ | Before v1.0 |
| **Front-desk / billing staff** | Shadow-and-coach for the first week | Go-live week |
| **IT / DBA** | Runbook walkthrough; backup/restore drill performed together | Pre go-live |
| **Compliance officer** | Audit-log demo; RBAC review | Pre go-live |
| **Patients (indirect)** | Signage / notice that records are now electronic; no UI exposure in v1 | Go-live week |

**Adoption KPIs** (tracked weekly for first 90 days):
- % of appointments booked through the system (target: ≥ 90% by week 4)
- % of encounters with a recorded diagnosis (target: ≥ 95% by week 4)
- % of invoices generated electronically (target: 100% by week 2)
- Daily active users by role (target: every role logs in daily)
- Support tickets per week (target: trending down after week 4)

### 1.19 At-a-Glance Summary

> **What:** A web app for small hospitals on top of an existing 52-table MySQL OLTP schema.
> **Who:** Receptionists, doctors, nurses, pharmacists, billers, managers, admins.
> **Six modules:** Appointments · EMR · Billing · Inventory · Staff · Reporting.
> **Hard rules:** Schema-authoritative · server-enforced RBAC · audit every PHI mutation · responsive desktop + tablet · WCAG 2.1 AA.
> **Positioning:** Epic Clarity for a 50-bed hospital, without the Epic price tag or 18-month rollout.
> **Timeline:** ~7 months from kickoff to a single-hospital pilot go-live.
> **Success:** A full patient visit recorded in ≤ 10 minutes by a trained user, p95 read latency < 300 ms, zero high security findings, 100% PHI mutations audit-logged, and the pilot department running on the system for 30 days without falling back to paper.

---

## 2. Human-Readable Prompt (Business Narrative)

> **Build a simple, secure, browser-based hospital management application for a small hospital.**
>
> The application must let front-desk staff register patients, schedule appointments, and check them in for visits. Doctors and nurses must be able to open a patient's chart, review their history, allergies, and active medications, and record what happened during today's encounter — vitals, diagnoses, procedures, and clinical notes. Doctors must be able to order labs and radiology studies, view results when they come back, and write prescriptions that the pharmacy can dispense and refill.
>
> Behind the scenes, the billing team must be able to generate invoices for each visit, file insurance claims, accept patient payments (cash, card, check, online), and follow up on outstanding balances. The pharmacy team must be able to manage medication inventory, watch for low stock and expiring lots, and place restocking orders. The administrator must be able to manage departments, rooms, beds, equipment, doctor schedules, nurse shifts, and user accounts.
>
> Everyone using the system should only see and do what their role allows. A receptionist should not see clinical notes. A doctor should not see another doctor's salary. Every change to a patient record must be logged so it can be audited later. The interface must work well on a desktop monitor at the nurses' station and on a tablet a doctor carries on rounds.
>
> Finally, the hospital leadership must be able to open a dashboard and see — at a glance — today's appointments, occupied beds, pending lab orders, outstanding invoices, low-stock medications, and doctor productivity, so they can make informed decisions without writing SQL queries.
>
> The system is **not** trying to compete with Epic. It is trying to give a small hospital 80% of the workflow value at 20% of the complexity.

---

## 3. Detailed Technical Prompt (Engineering Specification)

> **Design and implement a multi-tier, role-based web application on top of the existing `hospital_OLTP_system` MySQL 8.0+ schema. The system must expose all 11 domains and the 15 reporting views through a secure, audited REST API consumed by a responsive single-page front-end. The implementation must respect the schema's referential integrity rules, reuse the existing Python `DatabaseConnection` pattern, and enforce role-based access control on the server.**

### 3.1 System Architecture

#### 3.1.1 Logical Layers

```
┌────────────────────────────────────────────────────────────────┐
│  CLIENT  (browser, desktop ≥1280px / tablet ≥768px)            │
│  React 18+ SPA · TypeScript · React Router · TanStack Query     │
│  Tailwind / shadcn-ui · Zod schemas · Axios with interceptors   │
└──────────────────────────┬─────────────────────────────────────┘
                           │  HTTPS (TLS 1.2+), JWT bearer
                           ▼
┌────────────────────────────────────────────────────────────────┐
│  API GATEWAY  (Nginx / Caddy reverse proxy)                    │
│  Rate-limit · TLS termination · gzip · CORS · request logging   │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│  APPLICATION TIER  (FastAPI · Python 3.11)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Controllers   →  Services  →  Repositories  →  Models    │  │
│  │ (HTTP I/O)       (workflow)   (SQL/CRUD)       (Pydantic) │  │
│  └──────────────────────────────────────────────────────────┘  │
│  Cross-cutting: Auth, RBAC, Audit, Validation, Error Mapping   │
└──────────────────────────┬─────────────────────────────────────┘
                           │  mysql-connector-python (pooled)
                           ▼
┌────────────────────────────────────────────────────────────────┐
│  DATA TIER  (MySQL 8.0+)                                       │
│  52 tables · 82 FKs · 15 views · audit_logs · users/roles      │
└────────────────────────────────────────────────────────────────┘
```

#### 3.1.2 Recommended Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Backend framework | **FastAPI** (Python 3.11+) | Async, OpenAPI auto-gen, Pydantic validation, plays well with existing `database_connection.py` |
| ORM / DB access | **Raw SQL via `DatabaseConnection` + `pydantic` DTOs** | Schema is authoritative; ORMs add friction over 82 FKs and 15 views |
| Connection pool | **`mysql-connector-python` pool (size=20)** | Already in `requirements.txt`; extend `DatabaseConnection` with `pooling.MySQLConnectionPool` |
| Migrations | **Alembic** (or plain numbered `.sql` files in `migrations/`) | Reversible, version-controlled |
| Frontend framework | **React 18 + TypeScript + Vite** | Mature ecosystem; TypeScript catches contract drift early |
| State / data fetching | **TanStack Query** | Cache, retry, optimistic updates, mirrors REST nicely |
| UI components | **shadcn/ui + Tailwind CSS** | Accessible primitives (WCAG 2.1 AA), themeable |
| Form validation | **Zod (client) + Pydantic (server)** | Shared schema definitions, single source of truth via JSON schema export |
| Auth | **JWT (RS256) + refresh tokens in httpOnly cookie** | Stateless, supports SSO later |
| Password hashing | **argon2id (preferred)** or **bcrypt cost 12** | Modern, side-channel-resistant |
| Background jobs | **APScheduler** (in-process) for v1; **Celery + Redis** if scaled | Cron for appointment reminders, claim follow-ups |
| Observability | **structlog + Prometheus + Grafana** | Existing `Fake_Data_Log/` and `init_database_Setup/` patterns already emit timestamped logs |
| Containerization | **Docker Compose** (api, web, mysql) | Reproducible local dev mirroring `init_database_Setup.py` |

#### 3.1.3 Repository Layout (proposed)

```
hospital_OLTP_system/                       (existing)
├── backend/
│   ├── app/
│   │   ├── main.py                         # FastAPI entry
│   │   ├── config.py                       # Settings (reads from env, falls back to DB_CONFIG)
│   │   ├── database.py                     # Pool wrapper over DatabaseConnection
│   │   ├── auth/                           # JWT, password, RBAC decorators
│   │   ├── audit/                          # audit_logs writer middleware
│   │   ├── errors/                         # FK violation → 409, validation → 422
│   │   ├── domains/
│   │   │   ├── patients/                   # router · service · repository · schemas
│   │   │   ├── appointments/
│   │   │   ├── encounters/
│   │   │   ├── labs/
│   │   │   ├── radiology/
│   │   │   ├── pharmacy/
│   │   │   ├── insurance/
│   │   │   ├── billing/
│   │   │   ├── inventory/
│   │   │   ├── staff/
│   │   │   ├── reference/                  # ICD-10, CPT lookups
│   │   │   └── reports/                    # 15 views surfaced as endpoints
│   │   └── middleware/
│   ├── migrations/                         # numbered .sql files
│   └── tests/                              # pytest, hits a disposable test DB
├── frontend/
│   ├── src/
│   │   ├── api/                            # generated from OpenAPI
│   │   ├── pages/                          # 15 screens from §8.2
│   │   ├── components/                     # shared UI primitives
│   │   ├── features/                       # one folder per domain
│   │   ├── hooks/
│   │   ├── routes.tsx
│   │   └── auth/
│   └── package.json
├── docker-compose.yml
└── (existing files: create_schema.sql, database_views.sql, *.py, etc.)
```

---

### 3.2 API Surface — REST Conventions

#### 3.2.1 Naming & HTTP Semantics

| Verb | Path pattern | Returns | Use |
|---|---|---|---|
| `GET` | `/api/v1/{resource}` | `200` list (paginated) | List with filters |
| `GET` | `/api/v1/{resource}/{id}` | `200` object · `404` | Detail |
| `POST` | `/api/v1/{resource}` | `201` + `Location` header | Create |
| `PATCH` | `/api/v1/{resource}/{id}` | `200` object · `404` · `409` | Partial update |
| `DELETE` | `/api/v1/{resource}/{id}` | `204` · `404` · `409` | Soft-delete preferred; honors FK RESTRICT |
| `POST` | `/api/v1/{resource}/{id}:action` | `200` | Workflow transition (e.g. `appointments/123:cancel`) |
| `GET` | `/api/v1/reports/{view_name}` | `200` rows | Surface a database view |

#### 3.2.2 Standard Response Envelope

```jsonc
// Success
{
  "data": { /* object or array */ },
  "meta": { "page": 1, "page_size": 50, "total": 247 }
}

// Error
{
  "error": {
    "code": "FK_VIOLATION",          // stable machine code
    "message": "Cannot delete: doctor has active appointments",
    "field": "doctor_id",            // when applicable
    "details": { "constraint": "fk_appt_doctor" }
  }
}
```

#### 3.2.3 Error Code Catalog (non-exhaustive)

| HTTP | `code` | When |
|---|---|---|
| 400 | `BAD_REQUEST` | Malformed JSON, missing required field |
| 401 | `UNAUTHENTICATED` | No / expired JWT |
| 403 | `FORBIDDEN` | RBAC denial |
| 404 | `NOT_FOUND` | Resource doesn't exist or filtered out by row-level security |
| 409 | `CONFLICT` | Optimistic lock failure, duplicate unique key |
| 409 | `FK_VIOLATION` | MySQL error 1451/1452 mapped here |
| 409 | `WORKFLOW_INVALID_TRANSITION` | e.g. cancel an already-completed appointment |
| 422 | `VALIDATION_FAILED` | Pydantic schema rejection |
| 429 | `RATE_LIMITED` | Per-token rate limit hit |
| 500 | `INTERNAL` | Unhandled exception (logged with trace ID) |

#### 3.2.4 Pagination, Filtering, Sorting

- Cursor pagination preferred for `audit_logs`; offset pagination acceptable elsewhere.
- Query params: `?page=2&page_size=50&sort=-created_at&filter[status]=active&q=smith`.
- Server caps `page_size ≤ 200`.

#### 3.2.5 Endpoint Inventory (excerpt — full list in `/openapi.json`)

```
# Patients
GET    /api/v1/patients?q=&status=&page=&page_size=
POST   /api/v1/patients
GET    /api/v1/patients/{id}
PATCH  /api/v1/patients/{id}
GET    /api/v1/patients/{id}/encounters
GET    /api/v1/patients/{id}/allergies
POST   /api/v1/patients/{id}/allergies
GET    /api/v1/patients/{id}/insurance-policies

# Appointments
GET    /api/v1/appointments?date_from=&date_to=&doctor_id=&status=
POST   /api/v1/appointments
GET    /api/v1/appointments/{id}
PATCH  /api/v1/appointments/{id}
POST   /api/v1/appointments/{id}:confirm
POST   /api/v1/appointments/{id}:check-in
POST   /api/v1/appointments/{id}:cancel        # body: { reason, cancelled_by }
POST   /api/v1/appointments/{id}:reschedule    # body: { new_date, new_time, reason }

# Encounters
POST   /api/v1/encounters
GET    /api/v1/encounters/{id}
POST   /api/v1/encounters/{id}/vitals
POST   /api/v1/encounters/{id}/diagnoses       # body: { icd_code_id, type, severity }
POST   /api/v1/encounters/{id}/procedures      # body: { cpt_code_id, performed_by, ... }
POST   /api/v1/encounters/{id}/notes
POST   /api/v1/encounters/{id}:discharge

# Labs & Radiology
POST   /api/v1/lab-orders
GET    /api/v1/lab-orders/{id}
POST   /api/v1/lab-orders/{id}/tests
POST   /api/v1/lab-tests/{id}/result
POST   /api/v1/radiology-orders
POST   /api/v1/radiology-orders/{id}/result

# Pharmacy
POST   /api/v1/prescriptions
POST   /api/v1/prescriptions/{id}/refills
GET    /api/v1/medications?q=
GET    /api/v1/medication-inventory?low_stock=true
POST   /api/v1/pharmacy-orders

# Insurance & Billing
POST   /api/v1/insurance-claims
POST   /api/v1/insurance-claims/{id}:submit
POST   /api/v1/invoices
POST   /api/v1/invoices/{id}/items
POST   /api/v1/invoices/{id}/payments

# Reference
GET    /api/v1/icd-codes?q=
GET    /api/v1/cpt-codes?q=

# Reports (read-only, surface views)
GET    /api/v1/reports/active-doctors                # vw_active_doctors
GET    /api/v1/reports/todays-appointments           # vw_todays_appointments
GET    /api/v1/reports/upcoming-appointments         # vw_upcoming_appointments
GET    /api/v1/reports/active-encounters             # vw_active_encounters
GET    /api/v1/reports/active-prescriptions          # vw_active_prescriptions
GET    /api/v1/reports/available-beds                # vw_available_beds
GET    /api/v1/reports/bed-occupancy                 # vw_bed_occupancy
GET    /api/v1/reports/department-statistics         # vw_department_statistics
GET    /api/v1/reports/pending-lab-orders            # vw_pending_lab_orders
GET    /api/v1/reports/pending-radiology-orders      # vw_pending_radiology_orders
GET    /api/v1/reports/low-stock-medications         # vw_low_stock_medications
GET    /api/v1/reports/outstanding-invoices          # vw_outstanding_invoices
GET    /api/v1/reports/insurance-claims-summary      # vw_insurance_claims_summary
GET    /api/v1/reports/patient-summary               # vw_patient_summary
GET    /api/v1/reports/doctor-performance            # vw_doctor_performance

# Auth & Admin
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/users
POST   /api/v1/users
PATCH  /api/v1/users/{id}
GET    /api/v1/roles
GET    /api/v1/audit-logs?table_name=&user_id=&from=&to=
```

---

### 3.3 Workflow Engine — Transactional Sequences

Each workflow MUST execute inside a single MySQL transaction. On failure, rollback AND emit a structured error AND write a failed-attempt audit row.

#### 3.3.1 Patient Registration

```
BEGIN
  INSERT patients (...)                          → patient_id
  INSERT patient_addresses (patient_id, ...)     [≥ 1 row]
  INSERT patient_emergency_contacts (...)        [optional]
  INSERT patient_allergies (...)                 [optional]
  INSERT audit_logs (table='patients', action='INSERT', new_values=…)
COMMIT
```

**Validations:** MRN format `MRN\d{3,6}` and unique; DOB ≤ today; SSN unique if provided; at least one primary address.

#### 3.3.2 Appointment Lifecycle (state machine)

```
              ┌──────────┐
              │ scheduled│
              └────┬─────┘
       ┌──────────┼──────────┐
       ▼          ▼          ▼
  ┌────────┐ ┌─────────┐ ┌───────────┐
  │confirmed│ │cancelled│ │rescheduled│──► creates new scheduled
  └────┬───┘ └─────────┘ └───────────┘
       ▼
  ┌──────────┐
  │checked_in│
  └────┬─────┘
       ▼
  ┌───────────┐
  │in_progress│──► creates encounter
  └────┬──────┘
       ▼
  ┌─────────┐    ┌────────┐
  │completed│    │no_show │
  └─────────┘    └────────┘
```

**Booking validation (composable rules):**
1. Doctor must be `active` and have a `doctor_schedules` row covering `day_of_week` + `start_time/end_time`.
2. Doctor must have no other appointment overlapping `[appointment_time, appointment_time + duration_minutes)`.
3. `appointment_date >= CURDATE()`.
4. Patient must be `active`.
5. Room (if specified) must be `available`.

#### 3.3.3 Encounter → Orders → Results

```
ENCOUNTER (status='in_progress')
   ├── encounter_vitals (1..n)        ← nurse role
   ├── encounter_diagnoses (1..n)     ← doctor role (requires icd_code_id)
   ├── encounter_procedures (0..n)    ← doctor role (requires cpt_code_id)
   ├── clinical_notes (0..n)          ← doctor/nurse role (signed=true required to finalize)
   ├── lab_orders → lab_tests → lab_results
   ├── radiology_orders → radiology_results
   ├── prescriptions → prescription_refills
   └── bed_assignments                ← inpatient only
```

**Discharge precondition:** at least one diagnosis recorded AND any unsigned clinical_notes must be either signed or amended.

#### 3.3.4 Prescription → Inventory Decrement

```
BEGIN
  SELECT quantity_on_hand FROM medication_inventory
    WHERE medication_id=? FOR UPDATE          -- pessimistic lock
  IF quantity_on_hand < quantity_prescribed THEN
    RAISE 409 INSUFFICIENT_STOCK
  END IF
  INSERT prescriptions (...)
  UPDATE medication_inventory
    SET quantity_on_hand = quantity_on_hand - quantity_prescribed
  IF quantity_on_hand <= reorder_level THEN
    EMIT EVENT low_stock(medication_id)
  END IF
  INSERT audit_logs (...)
COMMIT
```

#### 3.3.5 Insurance Claim Lifecycle

```
draft → submitted → pending → ┬→ approved → paid (partially_paid possible)
                              ├→ denied  → appealed → (loops back to pending)
                              └→ partially_paid
```

#### 3.3.6 Billing Lifecycle

```
invoice (payment_status='pending')
   ├── invoice_items (1..n)           ← from encounter procedures, meds, room charges
   └── payment_transactions (0..n)    ← cash/check/card/insurance
       └── auto-recompute payment_status:
             amount_paid = 0           → pending
             0 < paid < total          → partial
             paid >= total             → paid
             due_date < today & due>0  → overdue
```

`amount_due` is a **generated stored column** in the schema — never write to it directly.

---

### 3.4 RBAC Matrix — Detailed Permissions

Permissions are stored as JSON in `roles.permissions` and evaluated by a FastAPI dependency. Each endpoint declares `required_permission: str`. The matrix below is the v1 default seed (insert into `roles` during initialization).

| Permission key | Receptionist | Nurse | Doctor | Pharmacist | Billing | Admin |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `patient:read` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `patient:write` | ✓ | — | ✓ | — | — | ✓ |
| `appointment:read` | ✓ | ✓ | ✓ | — | — | ✓ |
| `appointment:write` | ✓ | — | ✓ | — | — | ✓ |
| `encounter:read` | — | ✓ | ✓ | ✓¹ | — | ✓ |
| `encounter:write` | — | ✓² | ✓ | — | — | — |
| `vitals:write` | — | ✓ | ✓ | — | — | — |
| `diagnosis:write` | — | — | ✓ | — | — | — |
| `prescription:write` | — | — | ✓ | — | — | — |
| `prescription:dispense` | — | — | — | ✓ | — | — |
| `lab:order` | — | — | ✓ | — | — | — |
| `lab:result_entry` | — | — | ✓³ | — | — | — |
| `inventory:read` | — | — | — | ✓ | — | ✓ |
| `inventory:write` | — | — | — | ✓ | — | ✓ |
| `invoice:read` | — | — | — | — | ✓ | ✓ |
| `invoice:write` | — | — | — | — | ✓ | ✓ |
| `payment:record` | — | — | — | — | ✓ | ✓ |
| `claim:write` | — | — | — | — | ✓ | ✓ |
| `staff:read` | — | — | — | — | — | ✓ |
| `staff:write` | — | — | — | — | — | ✓ |
| `user:admin` | — | — | — | — | — | ✓ |
| `audit:read` | — | — | — | — | — | ✓ |
| `report:clinical` | — | ✓ | ✓ | — | — | ✓ |
| `report:financial` | — | — | — | — | ✓ | ✓ |
| `report:operational` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

¹ Pharmacist can read encounter to verify prescription context only.
² Nurses can write vitals, notes (type='nursing'), bed assignments — NOT diagnoses or procedures.
³ Lab result entry: lab tech role can be added in v2; for v1 doctors may enter manually.

**Row-level rule:** doctors see all patients (per "small hospital" assumption) but a future flag `roles.permissions.scope = 'own_patients'` can restrict to assigned panel.

---

### 3.5 Cross-Cutting Concerns

#### 3.5.1 Audit Logging Middleware

Every mutation passes through a decorator that:
1. Captures `old` row (SELECT before UPDATE/DELETE).
2. Captures `new` row (after the change).
3. Writes to `audit_logs` in the **same transaction** as the mutation.
4. Extracts `user_id` from JWT, `ip_address` from `X-Forwarded-For`, `user_agent` from header.
5. Encodes `old_values` / `new_values` as JSON (mask SSN, password_hash before serialization).

#### 3.5.2 Validation Layer

| Concern | Implementation |
|---|---|
| Schema validation | Pydantic models per endpoint; mirror to Zod on frontend via `datamodel-code-generator` |
| Business rules | Service-layer guards (e.g. `assert_no_overlap_for_doctor`) |
| DB constraints | UNIQUE, NOT NULL, CHECK, FK enforced — MySQL errors translated to user-friendly 4xx |
| Coded values | Foreign-key lookups to `icd_codes`, `cpt_codes`, `appointment_types`, `medications` — never free-text |

#### 3.5.3 Error Mapping (MySQL → HTTP)

| MySQL errno | HTTP | `code` |
|---|---|---|
| 1062 (duplicate key) | 409 | `DUPLICATE_KEY` |
| 1451 (FK delete restrict) | 409 | `FK_VIOLATION` |
| 1452 (FK insert/update missing) | 422 | `FK_REFERENCE_NOT_FOUND` |
| 1264 (out-of-range value) | 422 | `VALUE_OUT_OF_RANGE` |
| 1406 (data too long) | 422 | `FIELD_TOO_LONG` |
| 1048 (NOT NULL violation) | 422 | `MISSING_REQUIRED_FIELD` |
| 1213 (deadlock) | 503 | `RETRY_LATER` (server auto-retries 2x first) |

#### 3.5.4 Concurrency

- **Optimistic locking** via `updated_at` versioning on all mutable tables. Client sends `If-Unmodified-Since: <updated_at>`; mismatch → 409.
- **Pessimistic locking** (`SELECT … FOR UPDATE`) for inventory decrements and bed assignments.

#### 3.5.5 Caching

| Data | TTL | Strategy |
|---|---|---|
| ICD-10 / CPT lookups | 24 h | In-memory LRU; invalidate on POST/PATCH |
| Department / facility / room lists | 5 min | Same |
| Patient detail | none | Always fresh |
| Reports (views) | 60 s | Edge cache with bypass header for admins |

#### 3.5.6 Background Jobs (APScheduler)

| Job | Cadence | Purpose |
|---|---|---|
| `send_appointment_reminders` | every 15 min | T-24h and T-2h before scheduled appointments |
| `flag_overdue_invoices` | daily 02:00 | Set `payment_status='overdue'` where `due_date < today` |
| `expire_unverified_insurance` | daily 03:00 | Mark policies past `policy_end_date` |
| `inventory_expiry_scan` | daily 04:00 | Mark inventory with `expiration_date < today` as `expired` |
| `prune_audit_logs` | weekly | Archive logs older than retention window |

---

### 3.6 Performance, Scale & Reliability

| Target | Value | How measured |
|---|---|---|
| p95 read latency | < 300 ms | API gateway logs |
| p95 write latency | < 800 ms | Same |
| Dashboard render | < 1.5 s @ 500 rows | Browser perf API |
| Concurrent users | 50 | k6 / Locust load test |
| MySQL connection pool | 20 (min=5, max=40) | `mysql.connector.pooling` |
| Index coverage | every FK + every `status` ENUM | Already in `create_schema.sql` |
| Uptime SLO | 99.5% business hours | UptimeRobot / external monitor |
| RPO | ≤ 24 h (nightly dump) | Cron `mysqldump` to encrypted storage |
| RTO | ≤ 4 h | Restore drill quarterly |

**Query budget rules:**
- No N+1 queries — bulk fetch lookups (`WHERE id IN (...)`).
- Pagination mandatory for list endpoints (`LIMIT/OFFSET` with explicit `ORDER BY`).
- Long-running reports must run against the existing views (already optimized with joins).

---

### 3.7 Tech Constraints (Hard Rules)

1. **Do not bypass `database_connection.py` patterns.** Extend it for pooling; do not introduce a second connection style.
2. **Do not modify existing tables in place.** Any change is a numbered, reversible migration file in `migrations/`.
3. **Honor FK rules verbatim** (CASCADE / SET NULL / RESTRICT) — surface violations as user-friendly 409s.
4. **All timestamps stored in UTC**; rendered in the user's timezone (default `America/Chicago` per Springfield, IL sample data).
5. **Monetary values use `DECIMAL`**; never `FLOAT`. Round half-to-even at the boundary.
6. **No PHI in URLs, query strings, or logs.** PHI only in encrypted request bodies; logs receive a redacted form.
7. **Parameterized queries only.** Reject any code that interpolates user input into SQL.
8. **Initialization parity:** a fresh DB + `init_database_Setup.py` + `load_all_fake_data.py` must yield the same 500+ records used in dev and tests.
9. **Schema authority:** `create_schema.sql` is the source of truth; if a Pydantic model and the DDL disagree, fix the Pydantic model.
10. **No silent fallbacks.** If an insurance lookup fails, return 422 — never proceed with `NULL`.

---

### 3.8 Testing Strategy

| Layer | Tool | Coverage target |
|---|---|---|
| Unit (services) | pytest | 80% |
| Integration (API → DB) | pytest + disposable MySQL container | All workflow happy paths + each error code |
| Contract | schemathesis (from OpenAPI) | Auto-generated property tests |
| End-to-end | Playwright | The 8 acceptance workflows from §10 |
| Load | k6 | 50 concurrent users for 15 minutes |
| Security | bandit, pip-audit, npm audit, OWASP ZAP baseline | Zero highs |

Test data: `load_all_fake_data.py` against a `hospital_OLTP_system_test` DB recreated per CI run.

---

### 3.9 Deployment & Environments

| Env | DB | Frontend | API | Data |
|---|---|---|---|---|
| `local` | Docker MySQL | Vite dev server | `uvicorn --reload` | `load_all_fake_data.py` |
| `staging` | Managed MySQL | Built SPA on Caddy | gunicorn+uvicorn workers | scrubbed prod snapshot |
| `production` | Managed MySQL (replication) | CDN-served SPA | autoscaled API tier | live PHI — encrypted backups |

Promotion: `local → staging` on every merge to `main`; `staging → production` on tagged release after manual gate (admin + clinical sign-off).

---

## 4. Functional Modules

The docx identified six required modules. Each module below is specified at four levels:
1. **Purpose & User Stories** — what users get from the module, in narrative form.
2. **Capability Matrix** — backing tables and views.
3. **Workflows & Field-Level Specs** — step-by-step flows, screen elements, required vs optional fields, validation rules.
4. **Errors, Edge Cases, Permissions, and Test Scenarios** — what can go wrong, who can do what, and how we know it works.

> Module ordering reflects the typical clinical day: patient arrives (Appointments) → is seen (EMR) → is charged (Billing) — with supporting modules (Inventory, Staff, Reporting) wrapping around the core flow.

---

### 4.1 Appointment Scheduling

#### 4.1.1 Purpose
Allow front-desk staff (and, in future, patients) to **book, confirm, check in, reschedule, and cancel** appointments — with reminders, no double-booking, full audit trail, and visibility for clinicians of their day ahead.

#### 4.1.2 User Stories
- **As a receptionist**, I want to find a patient by MRN, name, or phone and book them an appointment with a specific doctor at a specific time, so I can complete a phone booking in under 60 seconds.
- **As a receptionist**, I want to see a calendar of all of today's appointments grouped by doctor, so I can check patients in as they arrive.
- **As a doctor**, I want to see my upcoming week at a glance with chief complaints, so I can prepare for each visit.
- **As a receptionist**, I want to reschedule an appointment without losing its history (audit trail and link to original), so we can prove no-shows or cancellations on demand.
- **As a patient (future)**, I want to get a reminder 24 hours and 2 hours before my visit, so I don't miss it.

#### 4.1.3 Capability Matrix

| Capability | Backing Tables | Backing Views | Primary Role |
|---|---|---|---|
| Find patient | `patients` | — | receptionist |
| Find doctor slot | `doctor_schedules`, `appointments` | `vw_upcoming_appointments` | receptionist |
| Book appointment | `appointments`, `appointment_types` | — | receptionist |
| Confirm appointment | `appointments` (status=confirmed) | — | receptionist, system |
| Check in | `appointments` (status=checked_in) | — | receptionist |
| Mark in-progress | `appointments` (status=in_progress) → creates `encounters` row | — | doctor / nurse |
| Complete | `appointments` (status=completed) | — | doctor |
| No-show | `appointments` (status=no_show) | — | receptionist |
| Reschedule | `appointments` (parent_appointment_id), `appointment_cancellations` | — | receptionist |
| Cancel | `appointment_cancellations` | — | receptionist, patient (future) |
| Today's queue | — | `vw_todays_appointments` | all clinical roles |
| Doctor's upcoming week | — | `vw_upcoming_appointments` | doctor |
| Reminders | (new) `appointment_reminders` — *backend table is v1 add* | — | system / scheduled job |

#### 4.1.4 Booking Workflow (happy path)

```
1. Receptionist searches for patient
   GET /api/v1/patients?q=...
2. Selects patient → opens booking modal
3. Selects appointment_type_id (defines default duration)
4. Picks date + doctor
   GET /api/v1/appointments/slots?doctor_id=X&date=Y
   → returns free slots derived from doctor_schedules ∩ existing appointments
5. Picks slot, enters reason / chief_complaint, optionally room
6. Submit
   POST /api/v1/appointments  (server validates rules 4.1.5)
7. System returns appointment_number (e.g. APT2026-00457)
8. Confirmation: receptionist optionally triggers SMS/email (v2)
```

#### 4.1.5 Booking Validation Rules

| # | Rule | Failure code | Failure message |
|---|---|---|---|
| BV-01 | `appointment_date >= today` | `VALIDATION_FAILED` | "Appointment date cannot be in the past." |
| BV-02 | Doctor `status='active'` | `VALIDATION_FAILED` | "This doctor is not currently active." |
| BV-03 | A row in `doctor_schedules` covers `day_of_week(appointment_date)` and `start_time/end_time` brackets the slot | `WORKFLOW_INVALID` | "The doctor is not scheduled at this time." |
| BV-04 | No other `appointments` row for `doctor_id` overlaps `[time, time + duration)` (excluding `cancelled` / `no_show`) | `CONFLICT` | "This slot is already booked." |
| BV-05 | Patient `status='active'` | `VALIDATION_FAILED` | "This patient's record is inactive." |
| BV-06 | If `room_id` set, room `status='available'` | `CONFLICT` | "Room not available." |
| BV-07 | `duration_minutes ∈ [10, 240]` | `VALIDATION_FAILED` | "Duration must be 10–240 minutes." |
| BV-08 | `priority` must be one of {routine, urgent, emergency} | `VALIDATION_FAILED` | "Invalid priority." |

#### 4.1.6 Field-Level Spec — Booking Form

| Field | Type | Required | Source / Constraint |
|---|---|---|---|
| Patient | autocomplete | ✓ | from `patients` |
| Doctor | select | ✓ | `doctors` where `status='active'` |
| Appointment type | select | ✓ | `appointment_types`; auto-sets `default_duration` |
| Date | date-picker | ✓ | ≥ today, within 6 months |
| Time | time-picker | ✓ | must fall in doctor's `doctor_schedules` window |
| Duration | integer (min) | ✓ | defaulted from type; editable 10–240 |
| Room | select | optional | `rooms` where `status='available'` |
| Priority | radio | ✓ | routine / urgent / emergency |
| Reason | text(255) | ✓ | free text |
| Chief complaint | text(text) | optional | richer free-text |
| Notes | text | optional | internal |

#### 4.1.7 State Machine

```
                  ┌──────────┐
            ┌────▶│scheduled │────cancel────► cancelled (audit row)
            │     └────┬─────┘
            │          │ confirm
            │          ▼
            │     ┌─────────┐
   reschedule     │confirmed│────no-show──► no_show
            │     └────┬────┘
            │          │ check_in
            │          ▼
            │     ┌──────────┐
            │     │checked_in│
            │     └────┬─────┘
            │          │ start (creates encounter)
            │          ▼
            │     ┌────────────┐
            │     │in_progress │
            │     └────┬───────┘
            │          │ complete
            │          ▼
            │     ┌─────────┐
            └─────│rescheduled│ (new row inherits parent_appointment_id)
                  └─────────┘
```

Transitions are gated server-side; the API rejects illegal transitions with `WORKFLOW_INVALID_TRANSITION`.

#### 4.1.8 Edge Cases & Errors

| Scenario | Behavior |
|---|---|
| Two receptionists try to book the same slot concurrently | Second booking fails with `CONFLICT` due to a unique constraint on `(doctor_id, appointment_date, appointment_time)` enforced at the application layer with `SELECT ... FOR UPDATE`. |
| Booking spans a doctor's break in `doctor_schedules` | Reject with `WORKFLOW_INVALID`. |
| Cancel an already-completed appointment | Reject with `WORKFLOW_INVALID_TRANSITION`. |
| Cancel an in-progress appointment | Reject; encounter must be discharged first. |
| Reschedule beyond 6 months | Reject with `VALIDATION_FAILED`. |
| Cancel within 2 hours | Allowed but flagged in `appointment_cancellations.notes`. |
| Patient inactive at check-in | Block check-in; require receptionist to reactivate (admin). |

#### 4.1.9 Permissions

| Action | receptionist | doctor | nurse | admin |
|---|:---:|:---:|:---:|:---:|
| List / view | ✓ | ✓ (own) | ✓ | ✓ |
| Book | ✓ | — | — | ✓ |
| Reschedule / cancel | ✓ | ✓ (own) | — | ✓ |
| Check in / no-show | ✓ | — | — | ✓ |
| Mark in-progress / complete | — | ✓ | — | ✓ |

#### 4.1.10 Test Scenarios

1. Book → confirm → check in → start → complete (happy path, < 60 seconds).
2. Two concurrent bookings on same slot → second receives `CONFLICT`.
3. Book outside `doctor_schedules` window → `WORKFLOW_INVALID`.
4. Cancel scheduled appointment → audit row created with `cancelled_by`, `reason`.
5. Reschedule → new row links via `parent_appointment_id`; original transitions to `rescheduled`.
6. Discharged appointment can no longer be cancelled.

---

### 4.2 Electronic Medical Records (EMR)

#### 4.2.1 Purpose
Provide clinicians a single, fast, audited view of a patient and let them **record what happened during a visit** — vitals, diagnoses (ICD-10-coded), procedures (CPT-coded), prescriptions, clinical notes, and orders for labs and imaging.

#### 4.2.2 User Stories
- **As a doctor**, when a patient is checked in, I want to open their chart and immediately see allergies, active medications, recent labs, and the last 5 encounters, so I have context within 5 seconds.
- **As a nurse**, I want to record a vitals set (BP, HR, temp, RR, SpO2, weight, height, pain) in under 60 seconds and have BMI auto-computed.
- **As a doctor**, I want to attach diagnoses to an encounter by typing the ICD-10 code or searching by description, so I never enter free-text-only diagnoses.
- **As a doctor**, I want to order labs from inside the encounter, see them come back in the same chart, and sign off on the results.
- **As a doctor**, I want to write a prescription with a structured medication picker (auto-completes from `medications`), have it check for allergies and interactions, and finalize it.
- **As a compliance officer**, I want every chart change recorded in `audit_logs` so I can prove who saw and changed what.

#### 4.2.3 Capability Matrix

| Capability | Backing Tables | Views |
|---|---|---|
| Patient summary | `patients`, `patient_allergies`, `patient_emergency_contacts` | `vw_patient_summary` |
| Encounter list | `encounters` | `vw_active_encounters` |
| Vitals | `encounter_vitals` | — |
| Diagnoses (ICD-10-coded) | `encounter_diagnoses` + `icd_codes` | — |
| Procedures (CPT-coded) | `encounter_procedures` + `cpt_codes` | — |
| Clinical notes (typed, signable) | `clinical_notes` | — |
| Bed assignment (inpatient) | `bed_assignments` | `vw_bed_occupancy` |
| Lab orders → results | `lab_orders`, `lab_tests`, `lab_results` | `vw_pending_lab_orders` |
| Radiology orders → results | `radiology_orders`, `radiology_results` | `vw_pending_radiology_orders` |
| Prescriptions | `prescriptions`, `prescription_refills`, `medications` | `vw_active_prescriptions` |
| Allergies | `patient_allergies` | — |

#### 4.2.4 Patient Chart — Required At-a-Glance View

When a clinician opens a patient (`GET /api/v1/patients/{id}`), the chart header MUST surface, within 1 second:

| Element | Source |
|---|---|
| Name, MRN, DOB, age (computed), gender, blood group, photo | `patients` |
| Active allergies with severity badge (life-threatening = red) | `patient_allergies WHERE status='active'` |
| Active prescriptions (medication, dose, frequency) | `vw_active_prescriptions` |
| Most recent vitals (timestamp + values) | `encounter_vitals ORDER BY recorded_datetime DESC LIMIT 1` |
| Last 5 encounters (date, type, doctor, primary diagnosis) | `encounters JOIN encounter_diagnoses WHERE diagnosis_type='primary'` |
| Abnormal lab results in last 30 days | `lab_results WHERE abnormal_flag != 'normal' AND result_datetime > now - 30d` |
| Primary insurance | `patient_insurance_policies WHERE is_primary` |
| Outstanding balance (badge) | `vw_outstanding_invoices` |

#### 4.2.5 Encounter Workflow

```
1. Trigger: appointment moves to "in_progress"  →  POST /api/v1/encounters
     body: { patient_id, doctor_id, appointment_id, encounter_type, chief_complaint, department_id, room_id }
     returns encounter_id (status='in_progress')

2. Nurse records vitals
     POST /api/v1/encounters/{id}/vitals
     server computes BMI if both weight + height present

3. Doctor adds diagnoses (1..n; exactly one must be 'primary')
     GET /api/v1/icd-codes?q=hyperten   →  picker
     POST /api/v1/encounters/{id}/diagnoses { icd_code_id, diagnosis_type, severity, ... }

4. Doctor adds procedures (0..n)
     GET /api/v1/cpt-codes?q=99213       →  picker
     POST /api/v1/encounters/{id}/procedures

5. Doctor orders labs / radiology (0..n)
     POST /api/v1/lab-orders          { encounter_id, tests:[{ test_code, ... }] }
     POST /api/v1/radiology-orders    { encounter_id, modality, body_part, ... }

6. Doctor writes prescriptions (0..n)
     POST /api/v1/prescriptions       (see §4.2.9 for allergy/interaction checks)

7. Doctor writes clinical note(s), signs
     POST /api/v1/encounters/{id}/notes { note_type, note_text, is_signed }

8. Discharge
     POST /api/v1/encounters/{id}:discharge { discharge_disposition, ... }
     preconditions: ≥ 1 primary diagnosis, all notes signed or amended, no unresolved orders for inpatient
     state → 'completed'
     appointment status → 'completed' (cascade)
```

Every step inside an open encounter writes an audit row.

#### 4.2.6 Vitals — Field Specs & Auto-Computation

| Field | Type | Range | Notes |
|---|---|---|---|
| `temperature` | decimal(4,1) °F | 90.0–110.0 | flag if outside 96.0–100.4 |
| `blood_pressure_systolic` | int | 60–250 | flag ≥ 140 or < 90 |
| `blood_pressure_diastolic` | int | 30–150 | flag ≥ 90 or < 60 |
| `heart_rate` | int | 30–220 | flag < 50 or > 120 |
| `respiratory_rate` | int | 5–60 | flag < 10 or > 25 |
| `oxygen_saturation` | decimal(5,2) % | 50.00–100.00 | flag < 92.00 |
| `weight` | decimal(5,2) lb | 1.00–800.00 | — |
| `height` | decimal(5,2) in | 10.00–96.00 | — |
| `bmi` | decimal(4,2) | computed | `(weight × 703) / (height²)` server-side |
| `pain_score` | int 0–10 | 0–10 | required if `chief_complaint` mentions pain |

Out-of-range values trigger inline warning but allow override with a recorded reason.

#### 4.2.7 Diagnosis Entry

- ICD-10 picker queries `icd_codes` (autocomplete by code or description).
- `diagnosis_type` ∈ {primary, secondary, differential, rule_out}. Exactly one `primary` per encounter at discharge.
- `severity` ∈ {mild, moderate, severe, critical}.
- `is_chronic` boolean — affects long-term problem list (future feature).
- Free-text `notes` allowed but **the ICD code is required** (FK to `icd_codes`).

#### 4.2.8 Procedure Entry

- CPT picker queries `cpt_codes`.
- `performed_by` defaults to current doctor, can be overridden.
- `anesthesia_type` if applicable.
- `complications` text — drives a flagged report.
- Linked to `encounters.encounter_id` (CASCADE on delete).

#### 4.2.9 Prescription — Allergy & Interaction Checks

Before persisting a prescription:

1. **Allergy check:** if `medications.medication_name` or `medications.generic_name` or `medications.drug_class` matches an active row in `patient_allergies` (drug type), return `CONFLICT` with details. Override allowed with explicit reason recorded in `prescriptions.indication`.
2. **Interaction check:** query `drug_interactions` for any (medication_id, other-active-rx.medication_id) pair. If `interaction_type='major'`, block with `CONFLICT`; if `moderate`, warn but allow; if `minor`, log only.
3. **Inventory check:** decrement `medication_inventory.quantity_on_hand` inside the transaction (see §3.3.4 lock pattern).
4. **Refill setup:** if `refills_allowed > 0`, set `refills_remaining = refills_allowed`.
5. **Audit:** write to `audit_logs` with full prescription JSON (mask future patient identifiers if cross-patient).

#### 4.2.10 Clinical Notes

- `note_type` ∈ {progress, admission, discharge, operative, consultation, nursing}.
- `author_type` ∈ {doctor, nurse, staff}.
- Signing flips `is_signed=TRUE`, sets `signed_datetime`. Signed notes are immutable; corrections create an **amendment** (`is_amended=TRUE`, `amendment_note` text). Amendments NEVER overwrite the original `note_text`.
- Audit log captures the signing event distinctly.

#### 4.2.11 Lab Order → Result

```
encounter →  lab_orders (1..n)
                ├── lab_tests (1..n per order)
                │       └── lab_results (1..1 per test, may be amended)
```

States: `ordered → collected → in_progress → completed (or cancelled)`.
Result entry surfaces `abnormal_flag` derived from reference range; UI shows red/yellow if abnormal.

#### 4.2.12 Edge Cases & Errors

| Scenario | Behavior |
|---|---|
| Discharge attempted with no primary diagnosis | Block with `WORKFLOW_INVALID`. |
| Note edited after signing | Block direct edit; allow `:amend` action only. |
| Same ICD code added twice as primary | Block — only one primary diagnosis. |
| Patient with life-threatening allergy receives prescription for that drug | Block with `CONFLICT`; override path requires a recorded reason and second factor. |
| Inventory insufficient at prescription time | Block (small hospital can't ignore stock); pharmacist must order. |
| Doctor opens another doctor's draft encounter | Allowed read-only unless covering provider (role flag). |

#### 4.2.13 Permissions

| Action | doctor | nurse | receptionist | pharmacist | admin |
|---|:---:|:---:|:---:|:---:|:---:|
| Read chart header | ✓ | ✓ | partial (no notes) | partial (Rx only) | ✓ |
| Create encounter | ✓ | — | — | — | ✓ |
| Write vitals | ✓ | ✓ | — | — | — |
| Add diagnosis | ✓ | — | — | — | — |
| Add procedure | ✓ | — | — | — | — |
| Order lab / radiology | ✓ | — | — | — | — |
| Write prescription | ✓ | — | — | — | — |
| Write clinical note | ✓ (any type) | ✓ (nursing only) | — | — | — |
| Sign note | ✓ (own) | ✓ (own) | — | — | — |
| Amend signed note | ✓ (own) | ✓ (own) | — | — | — |
| Discharge | ✓ | — | — | — | — |

#### 4.2.14 Test Scenarios

1. Open chart of a patient with 3 allergies → all 3 render with correct severity badge color.
2. Record vitals with weight=180 lb, height=70 in → BMI = 25.83 returned.
3. Discharge with no primary diagnosis → blocked.
4. Prescribe Amoxicillin to a patient with active Amoxicillin allergy → blocked, override prompt shown.
5. Sign a note, then attempt to edit → 409. Amend allowed → original preserved in audit log.
6. Concurrent doctors writing in same encounter → optimistic locking on `encounters.updated_at`.

---

### 4.3 Billing & Payments

#### 4.3.1 Purpose
Convert every encounter into a billable invoice, file insurance claims, and accept patient payments — with transparent line items, aging buckets, and accurate cash and insurance balances.

#### 4.3.2 User Stories
- **As a biller**, after an encounter completes, I want to one-click-generate an invoice from its procedures, meds, and room charges, so I never miss billable items.
- **As a biller**, I want to file an insurance claim from the encounter, with all CPT and ICD codes auto-populated.
- **As a receptionist or biller**, I want to accept a payment (cash, card, check, online) against an invoice and have the balance update immediately.
- **As a manager**, I want to see outstanding A/R by aging bucket (0–30, 31–60, 61–90, 90+ days), so I can prioritize collections.

#### 4.3.3 Capability Matrix

| Capability | Backing Tables | Views |
|---|---|---|
| Generate invoice from encounter | `invoices`, `invoice_items` | — |
| Add line item | `invoice_items` (links to `cpt_codes` for service items) | — |
| Record payment | `payment_transactions` | — |
| Adjust / write-off | `invoice_items.discount_amount`, status updates | — |
| Outstanding A/R + aging | — | `vw_outstanding_invoices` |
| File insurance claim | `insurance_claims`, `insurance_claim_items` | `vw_insurance_claims_summary` |
| Insurance authorization | `insurance_authorizations` | — |
| Patient insurance lookup | `patient_insurance_policies`, `insurance_plans`, `insurance_companies` | — |

#### 4.3.4 Invoice Generation Workflow

```
1. Trigger: encounter status → 'completed'
2. Biller opens encounter, clicks "Generate Invoice"
   POST /api/v1/invoices
     body: { encounter_id, patient_id, payment_terms, ... }
3. Server pulls line items:
     - encounter_procedures → invoice_items (item_type='procedure', cpt_code_id, unit_price from cpt.relative_value × hospital_rate)
     - prescriptions → invoice_items (item_type='medication', unit_price = medications.unit_price × quantity)
     - bed_assignments (inpatient) → invoice_items (item_type='room_charge', days × daily_rate)
     - lab_orders + radiology_orders → invoice_items
4. Subtotal, tax_amount, discount_amount, total_amount computed
5. amount_due is GENERATED column = total - amount_paid (never write directly)
6. payment_status set based on rules:
     amount_paid = 0 & due_date >= today          → 'pending'
     0 < amount_paid < total                       → 'partial'
     amount_paid >= total                          → 'paid'
     due_date < today AND amount_due > 0           → 'overdue' (auto via daily job)
```

#### 4.3.5 Payment Workflow

```
POST /api/v1/invoices/{id}/payments
  body: { payment_amount, payment_method, payment_reference, card_last_four (if card), ... }

Server rules:
1. payment_amount > 0
2. payment_amount <= amount_due  →  else 409 OVERPAYMENT (no implicit refunds in v1)
3. payment_method ∈ schema enum
4. Status auto-recomputed; receipt returned with new amount_due.
5. Audit row written.
```

#### 4.3.6 Insurance Claim Workflow

States: `draft → submitted → pending → {approved | denied | partially_paid} → paid → (appealed → pending loop)`.

| Step | Action |
|---|---|
| Draft | Biller creates claim from encounter (claim_items auto-populated from encounter_procedures + diagnoses). |
| Submit | `:submit` action validates: all CPT codes present, primary diagnosis present, patient insurance policy active on `service_date`. |
| Pending | Awaiting payer response. |
| Approved | Payer accepts; `allowed_amount`, `paid_amount`, `patient_responsibility` set. |
| Denied | Capture `denial_reason`; allow `:appeal` which creates a new submission. |
| Paid | When `paid_amount = allowed_amount`. |

#### 4.3.7 Aging Buckets (`vw_outstanding_invoices`)

Already implemented in the view:
- Current (≤ 0 days past due)
- Warning (1–30 days)
- Severe (31–60 days)
- Critical (> 90 days)

A/R dashboard shows totals and counts per bucket per patient and overall.

#### 4.3.8 Validation Rules

| # | Rule | Error |
|---|---|---|
| BL-01 | `total_amount = subtotal + tax_amount − discount_amount` | `VALIDATION_FAILED` |
| BL-02 | `amount_paid <= total_amount` | `OVERPAYMENT` |
| BL-03 | `due_date >= invoice_date` | `VALIDATION_FAILED` |
| BL-04 | At least one `invoice_items` row | `VALIDATION_FAILED` |
| BL-05 | Claim `service_date_from <= service_date_to` | `VALIDATION_FAILED` |
| BL-06 | Insurance policy active on `service_date_from` | `VALIDATION_FAILED` |
| BL-07 | Claim cannot submit without `≥ 1` ICD primary diagnosis | `WORKFLOW_INVALID` |

#### 4.3.9 Edge Cases & Errors

| Scenario | Behavior |
|---|---|
| Patient pays $50 on a $30 invoice | Block; explicit "refund" flow is out of scope v1. |
| Card processed externally; reference number absent | Allowed but flagged (`payment_reference IS NULL`) → reconciliation report picks up. |
| Insurance denied — appeal | Creates new submission preserving original claim chain. |
| Encounter retroactively edited after invoice exists | Block edit; require invoice void + re-issue (admin only). |
| Overdue auto-job runs on a paid invoice | No-op (idempotent). |

#### 4.3.10 Permissions

| Action | biller | receptionist | admin | doctor |
|---|:---:|:---:|:---:|:---:|
| Create invoice | ✓ | — | ✓ | — |
| Edit invoice line item | ✓ | — | ✓ | — |
| Apply discount | ✓ (≤ 10%); admin > 10% | — | ✓ | — |
| Record payment | ✓ | ✓ (cash/check at front desk) | ✓ | — |
| File claim | ✓ | — | ✓ | — |
| Void invoice | — | — | ✓ | — |

#### 4.3.11 Test Scenarios

1. Complete encounter with 2 procedures + 1 prescription → invoice has 3 line items, total_amount matches.
2. Two payments of $50 on a $120 invoice → status transitions pending → partial → partial; amount_due = $20.
3. Final $20 payment → status `paid`, amount_due = 0.
4. $30 payment on $20 invoice → blocked.
5. Submit claim missing ICD primary → blocked.
6. Claim denied → appeal creates new pending row, links to original.

---

### 4.4 Inventory Management

#### 4.4.1 Purpose
Keep medications and medical equipment available, fresh (not expired), and replenished — without stockouts during patient care.

#### 4.4.2 User Stories
- **As a pharmacist**, I want a dashboard of medications at or below reorder level and meds expiring within 90 days, so I can place restock orders today.
- **As a pharmacist**, I want to receive a restock delivery and update on-hand quantities lot-by-lot, so my counts stay accurate.
- **As a department manager**, I want to know which equipment is in my department, its last maintenance date, and warranty status.

#### 4.4.3 Capability Matrix

| Capability | Backing Tables | Views |
|---|---|---|
| Medication stock | `medication_inventory` | `vw_low_stock_medications` |
| Lot tracking & expiry | `medication_inventory.lot_number`, `expiration_date` | `vw_low_stock_medications` (days_to_expiry) |
| Restock order | `pharmacy_orders` | — |
| Receive delivery | `pharmacy_orders` (status update + inventory increment) | — |
| Equipment registry | `equipment` | — |
| Equipment assignment | `department_equipment` | — |
| Maintenance | `equipment.last_maintenance`, `next_maintenance` | — |

#### 4.4.4 Stock Decrement Hooks

| Event | Inventory effect |
|---|---|
| Prescription created | `medication_inventory.quantity_on_hand -= quantity_prescribed` (FOR UPDATE, see §3.3.4) |
| Prescription refill dispensed | Same as above per refill |
| Pharmacy order received | `quantity_on_hand += quantity_received`, set `last_restock_date / quantity` |
| Lot expires (daily job) | `status='expired'`; quantities excluded from available stock |
| Manual adjustment (admin) | Explicit `inventory_adjustments` row + reason in audit log |

#### 4.4.5 Alerts (server-emitted; surfaced in UI)

| Alert | Condition | Severity |
|---|---|---|
| Low stock | `quantity_on_hand <= reorder_level` | yellow |
| Critical stock | `quantity_on_hand < reorder_level / 2` | red |
| Expiry warning | `days_to_expiry <= 90` | yellow |
| Expired | `expiration_date < today` | red |
| Recall | `status='recalled'` | red |

#### 4.4.6 Restock Order Workflow

```
1. Pharmacist opens "low stock" view
2. Selects items, clicks "Create Pharmacy Order"
   POST /api/v1/pharmacy-orders
     body: { supplier_name, items:[{ medication_id, quantity_ordered, unit_cost }] }
3. Order status: 'pending'
4. After supplier confirmation: 'approved' → 'ordered'
5. Partial delivery:
   PATCH /api/v1/pharmacy-orders/{id}:receive { items:[{ id, quantity_received }] }
   status: 'partially_received'; inventory incremented; remainder still due
6. Full delivery → 'received'
```

#### 4.4.7 Equipment Workflow

| Capability | Detail |
|---|---|
| Register | `serial_number` UNIQUE; capture purchase + warranty dates |
| Assign | Insert `department_equipment` row; `return_date IS NULL` means active assignment |
| Move between departments | Close current assignment (set `return_date`), create new |
| Maintenance log | Update `last_maintenance`; set `next_maintenance` per `maintenance_schedule` |
| Retire | `equipment.status='retired'`; assignments must be closed |

#### 4.4.8 Validation Rules

| # | Rule | Error |
|---|---|---|
| IV-01 | `quantity_on_hand >= 0` always | enforce via `CHECK` or transaction guard |
| IV-02 | Cannot dispense from `expired` or `recalled` lot | `WORKFLOW_INVALID` |
| IV-03 | `expiration_date > today` for active lots | warn but allow new lot creation with future date only |
| IV-04 | Equipment with active assignment cannot be `retired` | `FK_VIOLATION` |

#### 4.4.9 Permissions

| Action | pharmacist | admin | doctor | nurse |
|---|:---:|:---:|:---:|:---:|
| View inventory | ✓ | ✓ | read-only | read-only |
| Adjust stock | ✓ | ✓ | — | — |
| Create pharmacy order | ✓ | ✓ | — | — |
| Receive delivery | ✓ | ✓ | — | — |
| Manage equipment | — | ✓ | — | — |

#### 4.4.10 Test Scenarios

1. Prescribe 30 tablets when 25 on hand → blocked with `INSUFFICIENT_STOCK`.
2. Prescribe 5 tablets when 10 on hand and reorder_level=10 → succeeds; UI shows "low stock" alert next refresh.
3. Lot A expires today → daily job sets status='expired'; UI hides from dispensable list.
4. Create pharmacy order → partial receive (40 of 50) → status='partially_received'; inventory increases by 40.
5. Retire equipment that's actively assigned to Cardiology → blocked.

---

### 4.5 Staff Management

#### 4.5.1 Purpose
Maintain accurate directories of doctors, nurses, and staff; manage weekly clinic schedules and shift patterns; track licensure and credential expiry; surface departmental staffing and doctor performance.

#### 4.5.2 User Stories
- **As an admin**, I want a single screen to add a new doctor with NPI, license, board certification, and department.
- **As a scheduler**, I want to set Dr. Smith's clinic hours as Mon–Fri 9–5 in Room 301, so the booking system honors those windows.
- **As a department manager**, I want to assign a nurse to a patient + bed for a shift, so handoffs are clear.
- **As a compliance officer**, I want a list of all clinicians whose license expires within 60 days.

#### 4.5.3 Capability Matrix

| Capability | Backing Tables | Views |
|---|---|---|
| Doctor directory | `doctors`, `specialists` | `vw_active_doctors` |
| Nurse directory | `nurses` | — |
| Staff directory | `staff` | — |
| Doctor weekly schedule | `doctor_schedules` | — |
| Staff / nurse shifts | `staff_shifts`, `nurse_assignments` | — |
| Department staffing rollup | `departments` | `vw_department_statistics` |
| Doctor performance (90-day) | — | `vw_doctor_performance` |
| Credential alerts | `doctors.license_expiry`, `doctors.board_certification` | — |

#### 4.5.4 Doctor Onboarding Workflow

```
1. Admin opens "Add Doctor"
2. Fills:
   - employee_id (UNIQUE)
   - first/last name
   - specialization + sub_specialization
   - department_id (FK)
   - license_number (UNIQUE), license_state, license_expiry
   - board_certification, medical_school, graduation_year
   - npi_number (UNIQUE)
   - consultation_fee
3. POST /api/v1/staff/doctors
4. Optional: add weekly schedule (next step)
5. Optional: mark as specialist (insert into `specialists`)
```

#### 4.5.5 Credential Expiry Indicators

| Window | Color | UI behavior |
|---|---|---|
| > 60 days | green | none |
| 14–60 days | yellow | warning badge on profile; weekly report |
| 0–14 days | red | warning on every encounter chart, blocks signing new prescriptions |
| Expired | red + block | block all clinical writes until renewal |

#### 4.5.6 Nurse Assignment Workflow

```
POST /api/v1/staff/nurse-assignments
  body: { nurse_id, patient_id, bed_id, shift, assigned_date, ... }

Server rules:
- Nurse status='active'
- Patient status='active'
- Bed status='occupied' AND patient currently in that bed
- No overlapping active assignment for the same nurse on a different patient in the same shift (warn but allow override)
```

End-of-shift: `PATCH /assignments/{id}` sets `end_date`.

#### 4.5.7 Validation Rules

| # | Rule | Error |
|---|---|---|
| SF-01 | `email` UNIQUE across all staff tables | `DUPLICATE_KEY` |
| SF-02 | `npi_number` exactly 10 digits | `VALIDATION_FAILED` |
| SF-03 | `license_expiry > today` at creation | `VALIDATION_FAILED` |
| SF-04 | `consultation_fee > 0` | `VALIDATION_FAILED` |
| SF-05 | Specialist requires existing doctor | `FK_REFERENCE_NOT_FOUND` |
| SF-06 | Cannot delete doctor with appointments / encounters / prescriptions | `FK_VIOLATION` (status='inactive' instead) |

#### 4.5.8 Permissions

| Action | admin | dept manager (future) | doctor | self |
|---|:---:|:---:|:---:|:---:|
| Add / edit doctor | ✓ | — | — | — |
| Set doctor schedule | ✓ | ✓ (own dept) | — | own (limited) |
| View directory | ✓ | ✓ | ✓ | ✓ |
| Edit own profile (phone, photo) | ✓ | ✓ | ✓ | ✓ |
| View salary fields | ✓ | — | — | own |

#### 4.5.9 Test Scenarios

1. Create doctor with duplicate NPI → blocked.
2. Doctor's license expires today → cannot sign new prescriptions until updated.
3. Assign nurse to patient who isn't in a bed → warning, allowed (outpatient).
4. Delete doctor with completed encounters → blocked; mark inactive instead.

---

### 4.6 Reporting & Analytics

#### 4.6.1 Purpose
Surface the 15 pre-built database views (plus a small number of computed metrics) as **role-tailored dashboards and exportable reports** — so leadership and clinicians can make decisions without writing SQL.

#### 4.6.2 User Stories
- **As an administrator**, I want a daily-census report by department (active encounters + bed occupancy) so I can match staffing to load.
- **As a department head**, I want a 90-day doctor productivity report so I can have one-on-ones with data.
- **As a CFO**, I want outstanding A/R by aging bucket and insurance claims summary so I can forecast cash.
- **As a pharmacist**, I want low-stock and expiry alerts so I can place orders.
- **As a compliance officer**, I want an audit-log export filtered by user, table, and date range.

#### 4.6.3 Report Catalog

| # | Report | Source view(s) | Key columns | Default filter |
|---|---|---|---|---|
| R-01 | Patient Flow / Census | `vw_active_encounters` + `vw_bed_occupancy` | dept, occupied beds, active encounters, days in facility | today |
| R-02 | Today's Appointments | `vw_todays_appointments` | time, patient, doctor, status | today |
| R-03 | Upcoming Appointments | `vw_upcoming_appointments` | date, patient, doctor, type, priority | next 7 days |
| R-04 | Active Doctors | `vw_active_doctors` | name, specialization, dept | active |
| R-05 | Doctor Performance (90-day) | `vw_doctor_performance` | total appts, completed, no-shows, avg duration, Rx count | last 90 days |
| R-06 | Department Statistics | `vw_department_statistics` | doctors, nurses, rooms, beds, equipment per dept | active depts |
| R-07 | Available Beds | `vw_available_beds` | facility, dept, bed | now |
| R-08 | Bed Occupancy | `vw_bed_occupancy` | patient, bed, days occupied, doctor, nurse | now |
| R-09 | Pending Lab Orders | `vw_pending_lab_orders` | order, patient, priority, total tests | active |
| R-10 | Pending Radiology Orders | `vw_pending_radiology_orders` | order, patient, modality, priority | active |
| R-11 | Active Prescriptions | `vw_active_prescriptions` | patient, medication, dosage, refills remaining | active |
| R-12 | Low Stock Medications | `vw_low_stock_medications` | name, on hand, reorder level, days to expiry | at/below threshold |
| R-13 | Outstanding Invoices (A/R) | `vw_outstanding_invoices` | patient, amount due, aging bucket | unpaid |
| R-14 | Insurance Claims Summary | `vw_insurance_claims_summary` | claim, payer, total/allowed/paid, status, days pending | last 90 days |
| R-15 | Patient Summary | `vw_patient_summary` | mrn, name, age, total encounters, last visit | active |
| R-16 (computed) | Lab Turnaround Time | `lab_orders.order_datetime` → `lab_results.result_datetime` (compute median + p95) | dept, modality, TAT median, p95 | last 30 days |
| R-17 (computed) | No-show Rate | `appointments` aggregate | doctor, total, no-shows, rate % | last 30 days |
| R-18 (computed) | Revenue by Department | join `invoices` ↔ `encounters` ↔ `departments` | dept, gross revenue, net, paid | this month |

#### 4.6.4 Common Capabilities (all reports)

- **Filters:** date range (preset: today, 7d, 30d, 90d, MTD, YTD, custom); department; role-specific fields.
- **Sort:** any column, ascending/descending.
- **Pagination:** server-side, `page_size ≤ 200`.
- **Export:** **CSV** (UTF-8 with BOM for Excel compatibility) and **PDF** (header with hospital name, report title, generated-at, filters applied).
- **Save view:** users can save a filter combination with a name (stored in user prefs).
- **Scheduled email** (v2): out of scope v1.

#### 4.6.5 Dashboard Tiles (role-tailored landing)

| Tile | For roles | Source |
|---|---|---|
| Today's appointments count + status breakdown | receptionist, doctor | R-02 |
| Active encounters by department | doctor, admin | R-01 |
| Outstanding A/R total + worst-aged | biller, admin | R-13 |
| Low-stock medications count | pharmacist | R-12 |
| Pending lab + radiology counts | doctor, admin | R-09, R-10 |
| Bed occupancy % | nurse, admin | R-07, R-08 |
| Credential expiry warnings | admin, compliance | computed from §4.5.5 |

#### 4.6.6 Performance & Caching

- Report endpoints cached **60 s** by default; bypass header `Cache-Control: no-cache` for admin "live" mode.
- Views run against indexed columns; if any report exceeds 1.5 s p95, add covering index or materialize in a daily job.
- Exports stream the result set (do not load all rows into memory).

#### 4.6.7 Permissions

| Report group | Roles |
|---|---|
| Operational (R-01, R-02, R-03, R-07, R-08, R-09, R-10) | all clinical + admin |
| Clinical (R-04, R-05, R-11, R-15, R-16) | doctor, admin, compliance |
| Financial (R-13, R-14, R-18) | biller, admin |
| Pharmacy (R-12) | pharmacist, admin |
| Staff (R-05, R-06, credential expiry) | admin |
| Audit (audit_logs export) | admin, compliance |

#### 4.6.8 Test Scenarios

1. Open dashboard as receptionist → sees R-02 tile, not R-13.
2. Filter R-13 to "Critical" aging bucket → only invoices > 90 days overdue.
3. Export R-05 to CSV → file opens in Excel with UTF-8 chars correct.
4. Export R-14 to PDF → header includes filters, footer includes page numbers.
5. Hit a 750-row report → renders < 1.5 s, paginated at 200/page.

---

### 4.7 Cross-Module Integration Notes

The six modules above are not silos — they integrate via the schema and through workflow triggers. Key cross-module flows:

| Source event | Downstream effect |
|---|---|
| Appointment → `in_progress` | Creates an `encounters` row in EMR |
| Encounter → `completed` | Unlocks "Generate Invoice" in Billing |
| Prescription saved | Decrements `medication_inventory` in Inventory; raises low-stock alert if applicable |
| Pharmacy order received | Increments `medication_inventory`; clears low-stock |
| Doctor license < 14 days from expiry | Blocks Rx signing in EMR |
| Insurance policy expired | Blocks claim submission in Billing |
| Bed assignment ends | Frees bed in Inventory/Org; auto-creates room-charge invoice line for the stay |
| Lab result `abnormal_flag='critical'` | Surfaces to ordering doctor's dashboard within 60 seconds |
| Encounter discharge | Cascades appointment to `completed`; finalizes notes; readies invoice |

These integrations MUST be implemented as **server-side workflow handlers** — never relied upon to fire from the client.

---

## 5. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Availability** | 99.5% uptime during business hours (a small hospital does not need 99.99%). |
| **Performance** | p95 read < 300 ms; p95 write < 800 ms; dashboard render < 1.5 s. |
| **Scalability** | Support 50 concurrent users, 500 patients, 5000 encounters/year. |
| **Browser support** | Latest 2 versions of Chrome, Edge, Safari, Firefox. |
| **Responsive** | Desktop (≥1280 px) and tablet (≥768 px). Mobile phone explicitly *out of scope* for v1. |
| **Accessibility** | WCAG 2.1 Level AA — keyboard navigation, contrast ratios, screen-reader labels on all forms. |
| **Localization** | English only for v1. Schema's `preferred_language` column is reserved for future. |
| **Backup** | Nightly MySQL dump; retention 30 days. |
| **Logging** | All mutations → `audit_logs`. Application logs to file + stdout. |

---

## 6. Domain & Database Mapping

(From the source docx, reconciled with the actual schema.)

| Domain | Tables | Description |
|---|---|---|
| Reference Data | 2 | ICD-10 and CPT coding standards |
| Organizational | 6 | Departments, facilities, rooms, beds, equipment, department_equipment |
| Patients | 4 | Patient records, addresses, emergency contacts, allergies |
| Providers | 8 | Doctors, nurses, staff, specialists, schedules, shifts, assignments |
| Appointments | 3 | Appointment types, appointments, cancellations |
| Clinical | 6 | Encounters, vitals, diagnoses, procedures, notes, bed assignments |
| Laboratory | 5 | Lab orders, tests, results, radiology orders, radiology results |
| Pharmacy | 6 | Medications, interactions, prescriptions, refills, inventory, pharmacy orders |
| Insurance | 7 | Companies, plans, policies, authorizations, claims, claim items |
| Billing | 3 | Invoices, invoice items, payment transactions |
| System | 4 | Users, roles, user_roles, audit_logs |
| **Total** | **54+** | (52 base + future appointment_reminders, notifications, etc.) |

> **Note:** The docx lists Providers as 7 tables; the implemented schema has 8 (includes `nurse_assignments`). The implemented schema is authoritative.

---

## 7. Security & Compliance

### 7.1 HIPAA-Ready Posture
- All PHI (name, DOB, SSN, MRN, diagnoses, prescriptions) encrypted in transit (TLS 1.2+) and at rest (MySQL encrypted tablespace or column-level encryption for SSN).
- **No PHI in URLs or query strings.** Patient IDs travel in request bodies / headers only.
- Session timeout: 15 minutes of inactivity for clinical users, 30 minutes for admin.
- Failed-login lockout: 5 attempts → 15-minute lock (use existing `users.failed_login_attempts`, `users.account_locked` columns).

### 7.2 Role-Based Access Control (RBAC)
Implemented via the existing `users → user_roles → roles` chain. Permissions stored as JSON in `roles.permissions`. **Enforce on the server, never the client.**

### 7.3 Audit Trail
Every `INSERT / UPDATE / DELETE / VIEW` on PHI writes a row to `audit_logs` with:
- `table_name`, `record_id`, `action`
- `user_id`, `user_type`
- `old_values` (JSON), `new_values` (JSON)
- `ip_address`, `user_agent`, `timestamp`

### 7.4 Data Protection
- SSN displayed as `***-**-1234` everywhere except the explicit "View SSN" admin action (which itself audits).
- Bulk export of patient data requires admin role + reason logged.

---

## 8. UI / UX Requirements

(From the docx + standard hospital UX patterns.)

### 8.1 Principles
- **Intuitive navigation** — left-rail global nav by module (Patients, Appointments, EMR, Pharmacy, Billing, Inventory, Staff, Reports).
- **Clear data entry forms** — labels above inputs, inline validation, required-field markers, sticky save bar.
- **Responsive layouts** — fluid grid, breakpoint at 1024 px (collapse left rail to icons), 1280 px+ default desktop.
- **Density toggle** — comfortable vs compact rows (clinicians on tablets need bigger touch targets; back-office users want density).
- **Speed** — keyboard shortcuts for power users (e.g., `g + p` → Patients, `n` → New).

### 8.2 Required Screens (v1)
1. Login / forgot password
2. Global dashboard (role-tailored: doctor sees today's schedule + pending labs; admin sees occupancy + A/R)
3. Patient list + search (by MRN, name, DOB, phone)
4. Patient detail / chart (tabs: Demographics, Insurance, Allergies, Encounters, Medications, Labs, Documents)
5. Appointment calendar (day / week views) + booking modal
6. Check-in workflow
7. Encounter screen (vitals → diagnoses → procedures → notes → orders → prescriptions)
8. Lab order entry + results review
9. Prescription entry + pharmacy dispensing queue
10. Inventory dashboard (low stock + expiring)
11. Invoice list + invoice detail + payment entry
12. Insurance claim list + claim detail
13. Staff directory + schedule editor
14. Reports hub (with the 6 reports listed above)
15. User & role admin

---

## 9. Integration Points

| Integration | Status in v1 | Notes |
|---|---|---|
| MySQL backend (existing) | **Required** | Reuse `database_connection.py`, do not bypass FK constraints. |
| Email (appointment reminders) | Optional | SMTP relay; out-of-scope if not provisioned. |
| SMS (reminders) | Out of scope | Future. |
| PACS (radiology images) | Out of scope | Schema has `radiology_results.image_location` stub. |
| HL7 / FHIR | Out of scope | Future. |
| Payment gateway | Out of scope | Cash/check/manual card entry only in v1. |
| Lab analyzer interface | Out of scope | Manual result entry in v1. |

---

## 10. Acceptance Criteria

The v1 release is accepted when:

1. **Workflows work end-to-end:**
   - Register a patient → book appointment → check in → create encounter → record vitals → enter diagnosis (ICD-10) → order lab → write prescription → check out → generate invoice → record payment. All in under 10 minutes for a single trained user.
2. **All six modules from the docx are operational** (Appointments, EMR, Billing, Inventory, Staff, Reporting).
3. **RBAC is enforced server-side** — a receptionist's session token cannot read `clinical_notes` via any API endpoint.
4. **Audit log captures every PHI mutation** with old/new JSON.
5. **All 15 existing database views are surfaced** as read-only analytics endpoints.
6. **Responsive layout verified** on a 1920×1080 desktop and a 1024×768 tablet.
7. **Performance targets met** under a load test of 50 concurrent users.
8. **Initialization is reproducible** — a fresh MySQL instance + `init_database_Setup.py` + `load_all_fake_data.py` + front-end deploy results in a working demo with 500+ test records.

---

## 11. Out of Scope (v1)

- Native mobile (iOS / Android) apps
- HL7 / FHIR interoperability
- PACS image viewing (DICOM)
- Real-time bed-management board (TV display)
- Telehealth / video visits
- Patient self-service portal (only staff-facing in v1)
- Predictive analytics / ML models
- Multi-tenant / multi-hospital deployment
- Multi-language UI (English only)

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **OLTP** | Online Transaction Processing — the transactional database supporting daily operations. |
| **EMR** | Electronic Medical Record — digital version of a patient's chart. |
| **MRN** | Medical Record Number — unique patient identifier within the hospital. |
| **NPI** | National Provider Identifier — unique US identifier for healthcare providers. |
| **ICD-10** | International Classification of Diseases, 10th revision — diagnosis codes. |
| **CPT** | Current Procedural Terminology — procedure / service codes used for billing. |
| **NDC** | National Drug Code — unique US identifier for medications. |
| **PHI** | Protected Health Information — patient identifying + medical data, governed by HIPAA. |
| **RBAC** | Role-Based Access Control. |
| **A/R** | Accounts Receivable — money owed to the hospital. |
| **DEA Schedule** | US Drug Enforcement Administration controlled-substance schedule (I–V). |
| **AMA** | Against Medical Advice (discharge disposition). |
| **PACS** | Picture Archiving and Communication System — radiology image storage. |

---

## Appendix A — Source Document

This requirements file is derived from `Design Analysis and Recommendations for Small Hospital Front.docx` (uploaded 2026-05-16) and reconciled against the implemented schema in `create_schema.sql`, `database_views.sql`, and the supporting Python initialization scripts.

## Appendix B — Reference Files

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project context and conventions for Claude Code |
| `README.md` | Project overview and quick start |
| `SCHEMA_DOCUMENTATION.md` | Complete technical schema reference |
| `ER_DIAGRAM.md` | Entity-relationship diagrams |
| `create_schema.sql` | 52 tables + 82 FK constraints (DDL) |
| `database_views.sql` | 15 reporting views |
| `database_connection.py` | DB connection manager (reuse for backend) |
| `init_database_Setup.py` | One-shot DB initialization |
| `load_all_fake_data.py` | 500+ record fake data loader |

---

## Appendix C — Additional Feature Requirements

*Source: `Additional_Feature.docx` (added 2026-05-17). These requirements extend the baseline specification above.*

### C.1 Vital Signs & Laboratory Work Capture

**Requirement.** Providers must be able to record both vital signs and laboratory work performed during patient care through a unified, structured capture interface. All clinical measurements shall be persisted in a normalized table that supports efficient tracking, querying, and downstream analysis.

**Data Model — Required Columns**

| Column | Purpose | Example |
|---|---|---|
| `measurement_type` | Type of vital sign or lab work being recorded | `blood_pressure_systolic`, `hemoglobin`, `temperature`, `glucose` |
| `unit_of_measurement` | Standardized unit for the recorded value | `mmHg`, `g/dL`, `°C`, `mg/dL` |
| `value` | Actual numeric/string value entered by the provider | `120`, `13.5`, `37.2`, `95` |

**Implementation Notes**
- The schema already contains `vital_signs` (Clinical domain) and `lab_results` (Laboratory domain); unification may be achieved either by a normalized `clinical_measurements` table or by ensuring consistent `(type, unit, value)` triplets across both existing tables.
- Lookup tables for `measurement_type` and `unit_of_measurement` are recommended to enforce standardization and enable reporting.
- Every measurement row must associate with the originating `encounter_id` and recording provider for traceability.

### C.2 Consolidated Final Requirements

The following functionalities are mandatory for the hospital application tool and supplement the detailed specifications in Sections 1–4 above.

| # | Requirement | Status vs. Existing Spec |
|---|---|---|
| C.2.1 | Record vital signs and laboratory work with `type`, `unit`, and `value` fields | New — see [C.1](#c1-vital-signs--laboratory-work-capture) |
| C.2.2 | Store patient identification details (name, MRN, contact info) alongside clinical data | Covered by `patients` table; reaffirmed here |
| C.2.3 | Secure provider authentication and role-based access control (RBAC) | Covered by `users`, `roles`, `user_roles`; reaffirmed |
| C.2.4 | Automatic time stamping of all entries (`created_at`, `updated_at`) | Covered by schema convention; reaffirmed |
| C.2.5 | Data export and reporting capabilities for clinical and administrative needs | **New** — see [C.3](#c3-data-export--reporting) |
| C.2.6 | Audit trail tracking all data modifications | Covered by `audit_logs`; reaffirmed |
| C.2.7 | Intuitive UI with navigation, search, and filtering | **New** — see [C.4](#c4-user-interface-enhancements) |

### C.3 Data Export & Reporting

**Requirement.** The application shall provide data export and summary reporting for clinical review, administrative needs, and audit purposes.

**Capability Matrix**

| Capability | Detail |
|---|---|
| Export formats | CSV, Excel (`.xlsx`), PDF (for printable summaries) |
| Exportable entities | Patient charts, encounter summaries, vital signs, lab results, billing statements, audit logs |
| Summary reports | Daily census, doctor performance (90-day), department statistics, credential expiry, A/R aging |
| Access control | Export actions logged to `audit_logs`; restricted by role (admin, doctor, billing) |
| PHI handling | Exports containing PHI must be watermarked with requester identity and timestamp |

### C.4 User Interface Enhancements

**Requirement.** The application shall present an intuitive interface that streamlines provider workflow.

| Feature | Behavior |
|---|---|
| Global navigation | Persistent sidebar with role-aware menu (patients, encounters, schedule, inventory, billing) |
| Search | Global search across patients (by MRN, name, DOB), encounters, and orders |
| Filtering | Column-level filters on all list views (status, date range, provider, department) |
| Sort & pagination | Server-side sort/pagination on all transactional list endpoints |
| Quick actions | Inline "Record Vitals", "Order Lab", "Prescribe" from the patient header |
| Accessibility | Keyboard navigable; WCAG 2.1 AA color contrast |

### C.5 Acceptance Criteria

1. A provider can record a complete set of vital signs and lab values for an encounter using the unified `(type, unit, value)` capture form, and the records are retrievable via the encounter view.
2. Every clinical entry is automatically time-stamped and attributable to an authenticated provider whose role permits the action.
3. An administrator can export a 30-day vitals dataset for a patient as CSV; the export action appears in `audit_logs` within the same session.
4. Any modification to a stored measurement is captured in the audit trail (old value, new value, modifier, timestamp).
5. A provider can locate any patient via global search using MRN or last name within 2 seconds on the standard dataset (~500 records).

### C.6 Schema & DDL Proposal

**Approach.** Introduce a unified `clinical_measurements` table that captures both vital signs and lab values via the `(type, unit, value)` triplet, with lookup tables for type and unit standardization. Existing `vital_signs` and `lab_results` tables remain for backward compatibility; new captures route through `clinical_measurements`.

**Lookup Tables**

```sql
CREATE TABLE measurement_types (
    type_id           INT AUTO_INCREMENT PRIMARY KEY,
    type_code         VARCHAR(50)  NOT NULL UNIQUE,            -- e.g., 'bp_systolic', 'hemoglobin'
    type_name         VARCHAR(150) NOT NULL,                   -- 'Blood Pressure (Systolic)'
    category          ENUM('vital_sign','lab','anthropometric','other') NOT NULL,
    loinc_code        VARCHAR(20),                             -- optional LOINC for interoperability
    default_unit_id   INT,
    normal_range_low  DECIMAL(10,3),
    normal_range_high DECIMAL(10,3),
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mtype_unit FOREIGN KEY (default_unit_id) REFERENCES measurement_units(unit_id)
);

CREATE TABLE measurement_units (
    unit_id     INT AUTO_INCREMENT PRIMARY KEY,
    unit_code   VARCHAR(20)  NOT NULL UNIQUE,                  -- 'mmHg', 'g/dL', 'mg/dL'
    unit_name   VARCHAR(100) NOT NULL,
    ucum_code   VARCHAR(20),                                   -- UCUM standard code
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Core Capture Table**

```sql
CREATE TABLE clinical_measurements (
    measurement_id    BIGINT AUTO_INCREMENT PRIMARY KEY,
    encounter_id      INT NOT NULL,
    patient_id        INT NOT NULL,                            -- denormalized for fast patient timeline
    type_id           INT NOT NULL,
    unit_id           INT NOT NULL,
    value_numeric     DECIMAL(15,4),                           -- preferred for numeric measurements
    value_text        VARCHAR(255),                            -- for qualitative results (e.g., 'positive')
    recorded_by       INT NOT NULL,                            -- FK -> users.user_id (provider)
    recorded_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_abnormal       BOOLEAN DEFAULT FALSE,                   -- computed against normal_range_*
    notes             TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_cm_encounter FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id),
    CONSTRAINT fk_cm_patient   FOREIGN KEY (patient_id)   REFERENCES patients(patient_id),
    CONSTRAINT fk_cm_type      FOREIGN KEY (type_id)      REFERENCES measurement_types(type_id),
    CONSTRAINT fk_cm_unit      FOREIGN KEY (unit_id)      REFERENCES measurement_units(unit_id),
    CONSTRAINT fk_cm_recorder  FOREIGN KEY (recorded_by)  REFERENCES users(user_id),

    CONSTRAINT chk_cm_value CHECK (value_numeric IS NOT NULL OR value_text IS NOT NULL),

    INDEX idx_cm_patient_recorded (patient_id, recorded_at DESC),
    INDEX idx_cm_encounter (encounter_id),
    INDEX idx_cm_type (type_id)
);
```

**Migration Note.** Seed `measurement_types` from existing vital sign columns (BP systolic/diastolic, HR, temp, RR, SpO₂, weight, height) and the most-used lab analytes. Backfill via a one-time script that pivots `vital_signs` rows into `clinical_measurements`.

### C.7 API Endpoint Specifications

All endpoints follow REST conventions, require JWT auth (`Authorization: Bearer <token>`), and emit audit log entries on writes.

**C.7.1 Record a Measurement**

```
POST /api/v1/encounters/{encounter_id}/measurements
Body:
{
  "type_code":     "bp_systolic",
  "unit_code":     "mmHg",
  "value_numeric": 128,
  "notes":         "post-exercise"
}
Response 201:
{
  "measurement_id": 90123,
  "is_abnormal":    false,
  "recorded_at":    "2026-05-17T14:22:00Z"
}
Errors: 400 INVALID_TYPE | 400 INVALID_UNIT | 403 FORBIDDEN | 404 ENCOUNTER_NOT_FOUND
```

**C.7.2 Bulk Record (Vitals Panel)**

```
POST /api/v1/encounters/{encounter_id}/measurements:bulk
Body: { "measurements": [ { ... }, { ... } ] }
Response 201: { "created": [ids], "failed": [{index, error}] }
```

**C.7.3 Retrieve Patient Timeline**

```
GET /api/v1/patients/{patient_id}/measurements
  ?type_code=hemoglobin&from=2026-01-01&to=2026-05-17&limit=50&offset=0
Response 200: { "items": [...], "total": 123, "limit": 50, "offset": 0 }
```

**C.7.4 Update / Correct a Measurement**

```
PATCH /api/v1/measurements/{measurement_id}
Body: { "value_numeric": 130, "notes": "corrected reading" }
Response 200: { ... updated record ... }
Behavior: previous values persisted in audit_logs (old_value, new_value, modifier, timestamp).
```

**C.7.5 Export**

```
GET /api/v1/exports/measurements
  ?patient_id=42&format=csv|xlsx|pdf&from=YYYY-MM-DD&to=YYYY-MM-DD
Response 200: streamed file with Content-Disposition: attachment
Side effect: audit_logs entry of type 'export' with row count, format, requester.
```

**C.7.6 Global Search**

```
GET /api/v1/search?q={query}&scope=patients|encounters|measurements&limit=20
Response 200: { "results": [ { type, id, label, snippet, url } ] }
Performance target: p95 < 500ms on ~500-record dataset (see C.5 #5).
```

### C.8 Validation Rules & Permissions

**C.8.1 Validation Rules**

| # | Rule | Error Code |
|---|---|---|
| CM-01 | `value_numeric` OR `value_text` must be present (not both null) | `MEASUREMENT_VALUE_REQUIRED` |
| CM-02 | `type_code` must exist in `measurement_types` and be active | `INVALID_TYPE` |
| CM-03 | `unit_code` must exist in `measurement_units` and be active | `INVALID_UNIT` |
| CM-04 | Numeric value within physiologically plausible range (per type) | `VALUE_OUT_OF_RANGE` |
| CM-05 | `encounter_id` must be in status `in_progress` or `completed` (not `cancelled`) | `ENCOUNTER_NOT_OPEN` |
| CM-06 | `recorded_by` must have a role with `measurement:write` permission | `FORBIDDEN` |
| CM-07 | Edit window: corrections allowed only within 24 hours of `recorded_at`; beyond that requires `measurement:admin_correct` | `EDIT_WINDOW_EXPIRED` |
| CM-08 | Export of >1000 rows requires `export:bulk` permission | `BULK_EXPORT_FORBIDDEN` |

**C.8.2 Permissions Matrix**

| Action | doctor | nurse | lab_tech | admin | billing |
|---|:---:|:---:|:---:|:---:|:---:|
| Record vitals | ✓ | ✓ | — | ✓ | — |
| Record lab result | ✓ | — | ✓ | ✓ | — |
| View own patients' measurements | ✓ | ✓ | ✓ | ✓ | — |
| View any patient's measurements | — | — | — | ✓ | — |
| Edit measurement (≤24h) | ✓ (own) | ✓ (own) | ✓ (own) | ✓ | — |
| Edit measurement (>24h) | — | — | — | ✓ | — |
| Delete measurement | — | — | — | ✓ | — |
| Export ≤1000 rows | ✓ | ✓ | ✓ | ✓ | ✓ |
| Export >1000 rows | — | — | — | ✓ | ✓ |
| View audit trail | — | — | — | ✓ | — |

### C.9 Test Scenarios

1. **Happy path — vitals capture.** Nurse logs in, opens active encounter, records BP 120/80, HR 72, Temp 36.8 °C via bulk endpoint. All three rows appear in `clinical_measurements` with `is_abnormal=false`, recorded_at within 2 seconds.
2. **Abnormal flagging.** Doctor records hemoglobin 7.5 g/dL (normal 12–16). System sets `is_abnormal=true`; encounter view highlights row in red.
3. **Invalid unit rejected.** POST measurement with `type_code='bp_systolic'`, `unit_code='g/dL'` → 400 `INVALID_UNIT`; nothing persisted.
4. **Edit window enforced.** Nurse attempts to correct a measurement 30 hours after `recorded_at` → 403 `EDIT_WINDOW_EXPIRED`. Admin then performs same edit → succeeds, old/new values in `audit_logs`.
5. **Cross-patient access blocked.** Doctor A (not assigned to Patient X) calls `GET /patients/{X}/measurements` → 403. Admin call succeeds.
6. **Export with audit.** Admin exports 90-day vitals for one patient as CSV (returns ~120 rows). File downloads; `audit_logs` contains one `export` entry with `row_count=120`, `format='csv'`, requester user_id.
7. **Bulk export gating.** Billing user requests export of measurements for 2000 encounters → 403 `BULK_EXPORT_FORBIDDEN`. Admin retries → succeeds.
8. **Global search performance.** Search `q=SMITH` against 500-patient dataset returns ≥1 patient result with p95 latency < 500ms across 20 sequential calls.
9. **Cancelled encounter blocked.** Attempt to record a measurement on an encounter with status='cancelled' → 400 `ENCOUNTER_NOT_OPEN`.
10. **Backfill integrity.** After running the `vital_signs → clinical_measurements` migration script, the row count of pivoted measurements equals (count of vital_signs rows × number of populated metric columns per row); spot-check 10 random rows match source values.
