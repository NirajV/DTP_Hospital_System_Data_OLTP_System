import type { Patient, Encounter, Measurement, MeasurementType, Diagnosis, ScheduleItem, Alert } from "./types";

export const MEASUREMENT_TYPES: MeasurementType[] = [
  { code: "bp_systolic",       name: "Blood Pressure (Systolic)",  unit: "mmHg",  low: 90,   high: 130 },
  { code: "bp_diastolic",      name: "Blood Pressure (Diastolic)", unit: "mmHg",  low: 60,   high: 85 },
  { code: "heart_rate",        name: "Heart Rate",                  unit: "bpm",   low: 60,   high: 100 },
  { code: "respiratory_rate",  name: "Respiratory Rate",            unit: "rpm",   low: 12,   high: 20 },
  { code: "temperature_f",     name: "Body Temperature",            unit: "°F",    low: 97.0, high: 99.5 },
  { code: "oxygen_saturation", name: "Oxygen Saturation (SpO₂)",    unit: "%",     low: 95,   high: 100 },
  { code: "weight_lb",         name: "Body Weight",                 unit: "lb",    low: null, high: null },
  { code: "height_in",         name: "Body Height",                 unit: "in",    low: null, high: null },
  { code: "pain_score",        name: "Pain Score",                  unit: "0–10",  low: 0,    high: 3 },
  { code: "hemoglobin",        name: "Hemoglobin",                  unit: "g/dL",  low: 12.0, high: 17.5 },
  { code: "glucose",           name: "Glucose (fasting)",           unit: "mg/dL", low: 70,   high: 99 },
  { code: "wbc",               name: "White Blood Cell Count",       unit: "K/µL",  low: 4.5,  high: 11.0 },
];

export const PATIENTS: Patient[] = [
  { id: 1, mrn: "MRN-1024", first: "Sarah",  last: "Chen",     dob: "1990-03-15", age: 34, sex: "F", blood: "O+",  phone: "(415) 555-0102", ins: "Aetna PPO",     pcp: "Dr. Julia Smith", status: "active",   alert: "Hemoglobin 7.5 g/dL (low)" },
  { id: 2, mrn: "MRN-1098", first: "Marcus", last: "Johnson",  dob: "1978-11-02", age: 46, sex: "M", blood: "A-",  phone: "(415) 555-0145", ins: "Blue Shield",   pcp: "Dr. Julia Smith", status: "active" },
  { id: 3, mrn: "MRN-1141", first: "Aisha",  last: "Patel",    dob: "1985-07-21", age: 38, sex: "F", blood: "B+",  phone: "(415) 555-0167", ins: "United Health", pcp: "Dr. Robert Kim",  status: "active" },
  { id: 4, mrn: "MRN-1156", first: "Diego",  last: "Ramirez",  dob: "1962-01-30", age: 63, sex: "M", blood: "O-",  phone: "(415) 555-0181", ins: "Medicare",      pcp: "Dr. Julia Smith", status: "active",   alert: "BP 162/98 (high)" },
  { id: 5, mrn: "MRN-1203", first: "Emily",  last: "O’Brien",  dob: "2001-09-12", age: 23, sex: "F", blood: "AB+", phone: "(415) 555-0194", ins: "Kaiser",        pcp: "Dr. Hannah Lee",  status: "active" },
  { id: 6, mrn: "MRN-1278", first: "Yuki",   last: "Tanaka",   dob: "1955-04-08", age: 70, sex: "F", blood: "A+",  phone: "(415) 555-0212", ins: "Medicare",      pcp: "Dr. Robert Kim",  status: "active" },
  { id: 7, mrn: "MRN-1311", first: "Liam",   last: "Walsh",    dob: "1994-12-19", age: 30, sex: "M", blood: "O+",  phone: "(415) 555-0228", ins: "Aetna PPO",     pcp: "Dr. Julia Smith", status: "active" },
  { id: 8, mrn: "MRN-1349", first: "Nadia",  last: "Hassan",   dob: "1971-06-04", age: 53, sex: "F", blood: "B-",  phone: "(415) 555-0241", ins: "Cigna",         pcp: "Dr. Hannah Lee",  status: "inactive" },
];

export const ENCOUNTERS_BY_PATIENT: Record<number, Encounter> = {
  1: { num: "ENC-7821", date: "2026-05-17 13:45", type: "outpatient",  status: "in_progress", doctor: "Dr. Julia Smith", complaint: "Fatigue, shortness of breath on exertion" },
  4: { num: "ENC-7805", date: "2026-05-17 11:10", type: "consultation", status: "in_progress", doctor: "Dr. Julia Smith", complaint: "Routine hypertension follow-up" },
};

export const VITALS: Record<number, Measurement[]> = {
  1: [
    { type: "Blood Pressure (Systolic)",  value: 120,  unit: "mmHg",  by: "Nurse Park", at: "14:22", status: "Normal" },
    { type: "Blood Pressure (Diastolic)", value: 80,   unit: "mmHg",  by: "Nurse Park", at: "14:22", status: "Normal" },
    { type: "Heart Rate",                  value: 78,   unit: "bpm",   by: "Nurse Park", at: "14:22", status: "Normal" },
    { type: "Temperature",                 value: 98.6, unit: "°F",    by: "Nurse Park", at: "14:22", status: "Normal" },
    { type: "Oxygen Saturation",           value: 98,   unit: "%",     by: "Nurse Park", at: "14:22", status: "Normal" },
    { type: "Hemoglobin",                  value: 7.5,  unit: "g/dL",  by: "Lab Tech",   at: "09:10", status: "Low" },
    { type: "White Blood Cell Count",      value: 8.2,  unit: "K/µL",  by: "Lab Tech",   at: "09:10", status: "Normal" },
    { type: "Glucose (fasting)",           value: 94,   unit: "mg/dL", by: "Lab Tech",   at: "09:10", status: "Normal" },
  ],
  4: [
    { type: "Blood Pressure (Systolic)",  value: 162,  unit: "mmHg", by: "Nurse Diaz", at: "11:08", status: "High" },
    { type: "Blood Pressure (Diastolic)", value: 98,   unit: "mmHg", by: "Nurse Diaz", at: "11:08", status: "High" },
    { type: "Heart Rate",                  value: 84,   unit: "bpm",  by: "Nurse Diaz", at: "11:08", status: "Normal" },
    { type: "Temperature",                 value: 98.2, unit: "°F",   by: "Nurse Diaz", at: "11:08", status: "Normal" },
  ],
};

export const DIAGNOSES: Record<number, Diagnosis[]> = {
  1: [
    { code: "D50.9",  text: "Iron deficiency anaemia",  severity: "moderate" },
    { code: "R53.83", text: "Other fatigue",            severity: "mild" },
  ],
  4: [
    { code: "I10",    text: "Essential hypertension",   severity: "moderate" },
    { code: "E78.5",  text: "Hyperlipidaemia",          severity: "mild" },
  ],
};

export const ALLERGIES: Record<number, string[]> = {
  1: ["Penicillin (rash)", "Sulfa drugs (hives)"],
  4: ["NSAIDs (GI upset)"],
};

export const TODAY: ScheduleItem[] = [
  { time: "09:00", patient: "Marcus Johnson",  reason: "Cardiology follow-up", room: "Rm 301", status: "completed" },
  { time: "10:00", patient: "Aisha Patel",     reason: "Annual physical",      room: "Rm 302", status: "completed" },
  { time: "11:00", patient: "Diego Ramirez",   reason: "BP check",             room: "Rm 301", status: "in_progress" },
  { time: "13:30", patient: "Sarah Chen",      reason: "Anaemia workup",       room: "Rm 305", status: "in_progress" },
  { time: "14:30", patient: "Liam Walsh",      reason: "Knee pain",            room: "Rm 304", status: "scheduled" },
  { time: "15:00", patient: "Emily O’Brien",   reason: "Vaccination",          room: "Rm 302", status: "scheduled" },
];

export const ALERTS: Alert[] = [
  { sev: "high", text: "Sarah Chen — Hemoglobin 7.5 g/dL (low)" },
  { sev: "high", text: "Diego Ramirez — BP 162/98 (stage 2 HTN)" },
  { sev: "med",  text: "Lab: 3 results pending review (>4h)" },
  { sev: "low",  text: "Credential: Dr. Kim license expires in 22d" },
];

export const ENCOUNTERS_BOARD = {
  in_progress: [
    { num: "ENC-7821", who: "Sarah Chen",    dr: "Dr. Smith", t: "13:45" },
    { num: "ENC-7805", who: "Diego Ramirez", dr: "Dr. Smith", t: "11:10" },
    { num: "ENC-7811", who: "Yuki Tanaka",   dr: "Dr. Kim",   t: "12:25" },
  ],
  completed: [
    { num: "ENC-7790", who: "Marcus Johnson", dr: "Dr. Smith", t: "09:32" },
    { num: "ENC-7794", who: "Aisha Patel",    dr: "Dr. Kim",   t: "10:48" },
  ],
  scheduled: [
    { num: "ENC-7830", who: "Liam Walsh",     dr: "Dr. Smith", t: "14:30" },
    { num: "ENC-7833", who: "Emily O’Brien",  dr: "Dr. Lee",   t: "15:00" },
    { num: "ENC-7841", who: "Nadia Hassan",   dr: "Dr. Lee",   t: "15:45" },
  ],
};

export const WEEK_ENCOUNTERS = [
  { day: "Mon", outpatient: 14, inpatient: 6, emergency: 3 },
  { day: "Tue", outpatient: 16, inpatient: 5, emergency: 4 },
  { day: "Wed", outpatient: 12, inpatient: 7, emergency: 2 },
  { day: "Thu", outpatient: 18, inpatient: 6, emergency: 5 },
  { day: "Fri", outpatient: 20, inpatient: 8, emergency: 3 },
  { day: "Sat", outpatient: 8,  inpatient: 3, emergency: 5 },
  { day: "Sun", outpatient: 10, inpatient: 4, emergency: 4 },
];

export const BED_OCCUPANCY = [
  { name: "ICU",        value: 18 },
  { name: "Surgery",    value: 12 },
  { name: "Cardio",     value: 22 },
  { name: "Pediatrics", value: 9  },
  { name: "Oncology",   value: 14 },
];
