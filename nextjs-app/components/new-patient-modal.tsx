"use client";

import { useEffect, useState } from "react";
import { X, ShieldCheck, RefreshCw } from "lucide-react";
import { createPatient, type CreatePatientBody } from "@/lib/api";
import type { Patient } from "@/lib/types";

const GENDERS = ["Male", "Female", "Other", "Prefer not to say"] as const;
const BLOOD_GROUPS = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

interface FormState {
  mrn: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  date_of_birth: string;
  gender: typeof GENDERS[number];
  phone: string;
  email: string;
  blood_group: string;
}

function emptyForm(): FormState {
  return {
    mrn: "",
    first_name: "",
    middle_name: "",
    last_name: "",
    date_of_birth: "",
    gender: "Female",
    phone: "",
    email: "",
    blood_group: "",
  };
}

function suggestMrn(): string {
  // MRN-XXXX (4-digit) — collision-checked server/mock-side at create
  const n = Math.floor(1000 + Math.random() * 9000);
  return `MRN-${n}`;
}

export function NewPatientModal({
  open,
  onClose,
  onCreated,
}: {
  open: boolean;
  onClose: () => void;
  onCreated: (p: Patient) => void;
}) {
  const [form, setForm] = useState<FormState>(emptyForm());
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (open) {
      setForm({ ...emptyForm(), mrn: suggestMrn() });
      setError(null);
      setFieldErrors({});
    }
  }, [open]);

  if (!open) return null;

  function update<K extends keyof FormState>(key: K, val: FormState[K]) {
    setForm((f) => ({ ...f, [key]: val }));
    setFieldErrors((e) => {
      if (!e[key as string]) return e;
      const { [key as string]: _drop, ...rest } = e;
      return rest;
    });
  }

  function validate(): boolean {
    const fe: Record<string, string> = {};
    if (!form.mrn.trim()) fe.mrn = "Required";
    if (!form.first_name.trim()) fe.first_name = "Required";
    if (!form.last_name.trim()) fe.last_name = "Required";
    if (!form.date_of_birth) fe.date_of_birth = "Required";
    else if (new Date(form.date_of_birth) > new Date()) fe.date_of_birth = "Cannot be in the future";
    setFieldErrors(fe);
    return Object.keys(fe).length === 0;
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!validate()) return;

    setSaving(true);
    const payload: CreatePatientBody = {
      mrn: form.mrn.trim(),
      first_name: form.first_name.trim(),
      middle_name: form.middle_name.trim() || undefined,
      last_name: form.last_name.trim(),
      date_of_birth: form.date_of_birth,
      gender: form.gender,
      phone: form.phone.trim() || undefined,
      email: form.email.trim() || undefined,
      blood_group: form.blood_group || undefined,
    };
    const res = await createPatient(payload);
    setSaving(false);

    if (!res.ok) {
      if (res.error === "MRN_CONFLICT") {
        setFieldErrors({ mrn: "MRN already in use" });
      } else {
        setError(res.detail || res.error || "Failed to create patient");
      }
      return;
    }
    if (res.patient) onCreated(res.patient);
    onClose();
  }

  return (
    <div className="fixed inset-0 z-40 bg-slate-900/40 grid place-items-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-2xl ring-soft overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <div className="font-semibold text-slate-900">New patient</div>
            <div className="text-xs text-slate-500">Register a new patient record</div>
          </div>
          <button onClick={onClose} className="p-1 rounded hover:bg-slate-100"><X className="w-5 h-5" /></button>
        </div>

        <form onSubmit={submit} className="px-6 py-5 space-y-5">
          {/* Identity */}
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Identity</div>
            <div className="grid grid-cols-6 gap-3">
              <Field label="MRN *" error={fieldErrors.mrn} className="col-span-3">
                <div className="flex gap-2">
                  <input
                    value={form.mrn}
                    onChange={(e) => update("mrn", e.target.value)}
                    placeholder="MRN-1234"
                    className="flex-1 px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm font-mono"
                  />
                  <button
                    type="button"
                    onClick={() => update("mrn", suggestMrn())}
                    className="px-2 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-500"
                    title="Suggest MRN"
                  >
                    <RefreshCw className="w-4 h-4" />
                  </button>
                </div>
              </Field>
              <Field label="Sex *" error={fieldErrors.gender} className="col-span-3">
                <select
                  value={form.gender}
                  onChange={(e) => update("gender", e.target.value as FormState["gender"])}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                >
                  {GENDERS.map((g) => <option key={g} value={g}>{g}</option>)}
                </select>
              </Field>

              <Field label="First name *" error={fieldErrors.first_name} className="col-span-2">
                <input
                  value={form.first_name}
                  onChange={(e) => update("first_name", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                />
              </Field>
              <Field label="Middle" className="col-span-2">
                <input
                  value={form.middle_name}
                  onChange={(e) => update("middle_name", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                />
              </Field>
              <Field label="Last name *" error={fieldErrors.last_name} className="col-span-2">
                <input
                  value={form.last_name}
                  onChange={(e) => update("last_name", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                />
              </Field>

              <Field label="Date of birth *" error={fieldErrors.date_of_birth} className="col-span-3">
                <input
                  type="date"
                  value={form.date_of_birth}
                  onChange={(e) => update("date_of_birth", e.target.value)}
                  max={new Date().toISOString().slice(0, 10)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                />
              </Field>
              <Field label="Blood group" className="col-span-3">
                <select
                  value={form.blood_group}
                  onChange={(e) => update("blood_group", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                >
                  {BLOOD_GROUPS.map((b) => <option key={b} value={b}>{b || "Unknown"}</option>)}
                </select>
              </Field>
            </div>
          </div>

          {/* Contact */}
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Contact</div>
            <div className="grid grid-cols-6 gap-3">
              <Field label="Phone" className="col-span-3">
                <input
                  value={form.phone}
                  onChange={(e) => update("phone", e.target.value)}
                  placeholder="(415) 555-0100"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                />
              </Field>
              <Field label="Email" className="col-span-3">
                <input
                  type="email"
                  value={form.email}
                  onChange={(e) => update("email", e.target.value)}
                  placeholder="patient@example.com"
                  className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
                />
              </Field>
            </div>
          </div>

          {error && (
            <div className="px-3 py-2 rounded-lg bg-rose-50 text-rose-700 text-sm border border-rose-100">
              {error}
            </div>
          )}

          <div className="flex items-center justify-between pt-2 border-t border-slate-100">
            <div className="text-xs text-slate-500 flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5" /> Audit-logged · creation timestamped
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={onClose}
                disabled={saving}
                className="px-4 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 disabled:opacity-50"
              >Cancel</button>
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700 disabled:opacity-60"
              >{saving ? "Saving…" : "Create patient"}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

function Field({
  label, error, className, children,
}: {
  label: string;
  error?: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={className}>
      <label className="text-xs font-medium text-slate-600">{label}</label>
      <div className="mt-1">{children}</div>
      {error && <div className="mt-1 text-[11px] text-rose-600">{error}</div>}
    </div>
  );
}
