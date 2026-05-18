// Types mirror the MySQL schema in ../../create_schema.sql and
// ../../create_schema_measurements.sql. Kept loose where the API
// reshapes columns (e.g., joins for measurement type/unit names).

export type Role = "doctor" | "nurse" | "lab_tech" | "admin" | "billing";

export type Sex = "M" | "F" | "Other";

export interface Patient {
  id: number;            // patients.patient_id
  mrn: string;
  first: string;
  last: string;
  dob: string;
  age: number;
  sex: Sex;
  blood?: string;
  phone?: string;
  ins?: string;          // insurance display label
  pcp?: string;          // primary care doctor display name
  status: "active" | "inactive";
  alert?: string;        // banner shown on patient header (e.g., "Hgb 7.5 low")
}

export type EncounterStatus = "scheduled" | "in_progress" | "completed" | "cancelled";

export interface Encounter {
  num: string;
  date: string;
  type: "outpatient" | "inpatient" | "emergency" | "surgical" | "consultation";
  status: EncounterStatus;
  doctor: string;
  complaint?: string;
}

export interface MeasurementType {
  code: string;            // type_code, e.g. 'bp_systolic'
  name: string;            // human-readable
  unit: string;            // default unit display
  low: number | null;
  high: number | null;
}

export type MeasurementStatus = "Normal" | "Low" | "High";

export interface Measurement {
  type: string;            // type_name
  value: number | string;
  unit: string;            // unit_code display
  by: string;              // recorded_by display
  at: string;              // recorded_at display
  status: MeasurementStatus;
}

export interface Diagnosis {
  code: string;
  text: string;
  severity: "mild" | "moderate" | "severe" | "critical";
}

export interface ScheduleItem {
  time: string;
  patient: string;
  reason: string;
  room: string;
  status: EncounterStatus;
}

export interface Alert {
  sev: "high" | "med" | "low";
  text: string;
}

// API request / response shapes (subset — matches api/measurements_api.py)

export interface RecordMeasurementBody {
  type_code: string;
  unit_code: string;
  value_numeric?: number;
  value_text?: string;
  notes?: string;
}

export interface RecordMeasurementResponse {
  measurement_id: number;
  is_abnormal: boolean;
  recorded_at: string;
}

export interface SearchResult {
  type: string;
  id: number;
  label: string;
  snippet?: string;
  url: string;
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  scope: string;
}
