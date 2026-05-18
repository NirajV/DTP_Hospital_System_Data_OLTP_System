"use client";

import { useState } from "react";
import { X, Plus, Trash2, ShieldCheck } from "lucide-react";
import { MEASUREMENT_TYPES } from "@/lib/mock-data";
import { bulkRecordMeasurements } from "@/lib/api";
import type { Measurement, MeasurementStatus } from "@/lib/types";

interface Row {
  code: string;
  value: string;
}

function emptyRow(): Row {
  return { code: MEASUREMENT_TYPES[0].code, value: "" };
}

function statusFor(code: string, value: number): MeasurementStatus {
  const t = MEASUREMENT_TYPES.find((m) => m.code === code);
  if (!t) return "Normal";
  if (t.low != null && value < t.low) return "Low";
  if (t.high != null && value > t.high) return "High";
  return "Normal";
}

export function RecordVitalsModal({
  open,
  onClose,
  patientLabel,
  encounterNum,
  encounterId,
  onSaved,
}: {
  open: boolean;
  onClose: () => void;
  patientLabel: string;
  encounterNum: string;
  encounterId: number;
  onSaved: (rows: Measurement[]) => void;
}) {
  const [rows, setRows] = useState<Row[]>([emptyRow(), emptyRow(), emptyRow()]);
  const [notes, setNotes] = useState("");

  if (!open) return null;

  function update(idx: number, patch: Partial<Row>) {
    setRows((rs) => rs.map((r, i) => (i === idx ? { ...r, ...patch } : r)));
  }
  function add() { setRows((rs) => [...rs, emptyRow()]); }
  function remove(idx: number) { setRows((rs) => rs.filter((_, i) => i !== idx)); }

  async function save(e: React.FormEvent) {
    e.preventDefault();
    const filled = rows.filter((r) => r.value !== "");
    const apiPayload = filled.map((r) => {
      const t = MEASUREMENT_TYPES.find((m) => m.code === r.code)!;
      return {
        type_code: r.code,
        unit_code: t.unit,
        value_numeric: parseFloat(r.value),
        notes: notes || undefined,
      };
    });
    // best-effort backend write (no-op in mock mode)
    await bulkRecordMeasurements(encounterId, apiPayload);

    const optimistic: Measurement[] = filled.map((r) => {
      const t = MEASUREMENT_TYPES.find((m) => m.code === r.code)!;
      const num = parseFloat(r.value);
      return {
        type: t.name,
        value: num,
        unit: t.unit,
        by: "Dr. Julia Smith",
        at: new Date().toTimeString().slice(0, 5),
        status: statusFor(r.code, num),
      };
    });
    onSaved(optimistic);
    onClose();
    setRows([emptyRow(), emptyRow(), emptyRow()]);
    setNotes("");
  }

  return (
    <div className="fixed inset-0 z-40 bg-slate-900/40 grid place-items-center p-4">
      <div className="w-full max-w-3xl bg-white rounded-2xl ring-soft overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <div className="font-semibold text-slate-900">Record clinical measurements</div>
            <div className="text-xs text-slate-500">{patientLabel} · Encounter {encounterNum}</div>
          </div>
          <button onClick={onClose} className="p-1 rounded hover:bg-slate-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={save} className="px-6 py-5 space-y-4">
          <div className="grid grid-cols-12 gap-2 text-xs uppercase tracking-wider text-slate-500 px-1">
            <div className="col-span-5">Measurement type</div>
            <div className="col-span-3">Value</div>
            <div className="col-span-3">Unit</div>
            <div className="col-span-1" />
          </div>

          <div className="space-y-2">
            {rows.map((row, idx) => {
              const t = MEASUREMENT_TYPES.find((m) => m.code === row.code)!;
              return (
                <div key={idx} className="grid grid-cols-12 gap-2 items-center">
                  <select
                    value={row.code}
                    onChange={(e) => update(idx, { code: e.target.value })}
                    className="col-span-5 px-3 py-2 rounded-lg border border-slate-200 text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
                  >
                    {MEASUREMENT_TYPES.map((m) => (
                      <option key={m.code} value={m.code}>{m.name}</option>
                    ))}
                  </select>
                  <input
                    value={row.value}
                    onChange={(e) => update(idx, { value: e.target.value })}
                    placeholder="e.g. 120"
                    inputMode="decimal"
                    className="col-span-3 px-3 py-2 rounded-lg border border-slate-200 text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
                  />
                  <input
                    value={t.unit}
                    readOnly
                    className="col-span-3 px-3 py-2 rounded-lg border border-slate-200 bg-slate-50 text-sm"
                  />
                  <button
                    type="button"
                    onClick={() => remove(idx)}
                    className="col-span-1 p-2 text-slate-400 hover:text-rose-600"
                    aria-label="Remove row"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              );
            })}
          </div>

          <button type="button" onClick={add} className="text-xs text-brand-600 hover:underline flex items-center gap-1">
            <Plus className="w-3.5 h-3.5" /> Add another measurement
          </button>

          <div>
            <label className="text-xs font-medium text-slate-600">Notes (optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={2}
              className="mt-1 w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
            />
          </div>

          <div className="flex items-center justify-between pt-2 border-t border-slate-100">
            <div className="text-xs text-slate-500 flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5" />
              Audit-logged · timestamped automatically
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50"
              >Cancel</button>
              <button
                type="submit"
                className="px-4 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700"
              >Save measurements</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
