// Typed API client. Each call attempts the Flask backend and falls back
// to mock data on failure (or when NEXT_PUBLIC_USE_MOCK=true). This lets
// the UI demo without a backend running.

import {
  PATIENTS,
  VITALS,
  ENCOUNTERS_BY_PATIENT,
  DIAGNOSES,
  ALLERGIES,
} from "./mock-data";
import type {
  Patient,
  Measurement,
  RecordMeasurementBody,
  RecordMeasurementResponse,
  SearchResponse,
  SearchResult,
} from "./types";

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK !== "false";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8080";

function authHeaders(): HeadersInit {
  if (typeof window === "undefined") return {};
  return {
    "X-User-Id": localStorage.getItem("user_id") || "1",
    "X-User-Role": localStorage.getItem("user_role") || "doctor",
    "Content-Type": "application/json",
  };
}

async function tryFetch<T>(path: string, init?: RequestInit): Promise<T | null> {
  if (USE_MOCK) return null;
  try {
    const res = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: { ...authHeaders(), ...(init?.headers || {}) },
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

// -------- Search --------

export async function searchPatients(q: string, limit = 8): Promise<SearchResult[]> {
  if (!q) return [];
  const real = await tryFetch<SearchResponse>(
    `/api/v1/search?q=${encodeURIComponent(q)}&scope=patients&limit=${limit}`
  );
  if (real) return real.results;

  const needle = q.toLowerCase();
  return PATIENTS.filter(
    (p) =>
      p.first.toLowerCase().includes(needle) ||
      p.last.toLowerCase().includes(needle) ||
      p.mrn.toLowerCase().includes(needle)
  )
    .slice(0, limit)
    .map((p) => ({
      type: "patient",
      id: p.id,
      label: `${p.last}, ${p.first} (${p.mrn})`,
      snippet: `DOB ${p.dob}`,
      url: `/patients/${p.id}`,
    }));
}

// -------- Patients --------

export async function listPatients(): Promise<Patient[]> {
  const real = await tryFetch<{ items: Patient[] }>("/api/v1/patients?limit=500");
  if (real) return real.items;
  return PATIENTS;
}

export async function getPatient(id: number): Promise<Patient | undefined> {
  const real = await tryFetch<Patient>(`/api/v1/patients/${id}`);
  if (real) return real;
  return PATIENTS.find((p) => p.id === id);
}

export interface CreatePatientBody {
  mrn: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  date_of_birth: string;          // YYYY-MM-DD
  gender: "Male" | "Female" | "Other" | "Prefer not to say";
  phone?: string;
  email?: string;
  blood_group?: string;
}

export interface CreatePatientResult {
  ok: boolean;
  patient?: Patient;
  error?: string;
  detail?: string;
}

function calcAge(dob: string): number {
  const d = new Date(dob);
  const t = new Date();
  let age = t.getFullYear() - d.getFullYear();
  const m = t.getMonth() - d.getMonth();
  if (m < 0 || (m === 0 && t.getDate() < d.getDate())) age -= 1;
  return age;
}

export async function createPatient(body: CreatePatientBody): Promise<CreatePatientResult> {
  // Try real backend first
  if (!USE_MOCK) {
    try {
      const res = await fetch(`${API_URL}/api/v1/patients`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(body),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) return { ok: true, patient: data as Patient };
      return { ok: false, error: data.error || "REQUEST_FAILED", detail: data.detail };
    } catch (e) {
      return { ok: false, error: "NETWORK_ERROR", detail: String(e) };
    }
  }

  // Mock mode: validate uniqueness and append
  if (PATIENTS.some((p) => p.mrn === body.mrn)) {
    return { ok: false, error: "MRN_CONFLICT" };
  }
  const sexMap: Record<string, "M" | "F" | "Other"> = {
    Male: "M", Female: "F", Other: "Other", "Prefer not to say": "Other",
  };
  const newPatient: Patient = {
    id: Math.max(0, ...PATIENTS.map((p) => p.id)) + 1,
    mrn: body.mrn,
    first: body.first_name,
    last: body.last_name,
    dob: body.date_of_birth,
    age: calcAge(body.date_of_birth),
    sex: sexMap[body.gender] || "Other",
    blood: body.blood_group,
    phone: body.phone,
    status: "active",
  };
  PATIENTS.push(newPatient);
  return { ok: true, patient: newPatient };
}

export function getCurrentEncounter(patientId: number) {
  return ENCOUNTERS_BY_PATIENT[patientId];
}

export function getDiagnoses(patientId: number) {
  return DIAGNOSES[patientId] || [];
}

export function getAllergies(patientId: number): string[] {
  return ALLERGIES[patientId] || [];
}

// -------- Measurements --------

export async function getPatientMeasurements(patientId: number): Promise<Measurement[]> {
  const real = await tryFetch<{ items: Measurement[] }>(
    `/api/v1/patients/${patientId}/measurements?limit=100`
  );
  if (real) return real.items;
  return VITALS[patientId] || [];
}

export async function recordMeasurement(
  encounterId: number,
  body: RecordMeasurementBody
): Promise<RecordMeasurementResponse | null> {
  return tryFetch<RecordMeasurementResponse>(
    `/api/v1/encounters/${encounterId}/measurements`,
    { method: "POST", body: JSON.stringify(body) }
  );
}

export async function bulkRecordMeasurements(
  encounterId: number,
  measurements: RecordMeasurementBody[]
): Promise<{ created: number[]; failed: { index: number; error: string }[] } | null> {
  return tryFetch(`/api/v1/encounters/${encounterId}/measurements:bulk`, {
    method: "POST",
    body: JSON.stringify({ measurements }),
  });
}

// -------- Export --------

export function exportMeasurementsUrl(
  patientId: number,
  format: "csv" | "xlsx" | "pdf" = "csv",
  from?: string,
  to?: string
): string {
  const params = new URLSearchParams({ patient_id: String(patientId), format });
  if (from) params.set("from", from);
  if (to) params.set("to", to);
  return `${API_URL}/api/v1/exports/measurements?${params.toString()}`;
}
