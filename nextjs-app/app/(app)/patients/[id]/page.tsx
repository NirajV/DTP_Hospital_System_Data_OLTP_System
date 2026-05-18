"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ChevronRight, CalendarPlus, Activity, FilePlus, Download, Plus,
} from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import { StatusBadge } from "@/components/status-badge";
import { RecordVitalsModal } from "@/components/record-vitals-modal";
import {
  getPatient, getPatientMeasurements, getCurrentEncounter,
  getDiagnoses, getAllergies, exportMeasurementsUrl,
} from "@/lib/api";
import { initials, avatarColor, cn } from "@/lib/utils";
import type { Patient, Measurement } from "@/lib/types";

const TABS = [
  { key: "overview",   label: "Overview" },
  { key: "vitals",     label: "Vitals & Labs" },
  { key: "encounters", label: "Encounters" },
  { key: "meds",       label: "Medications" },
  { key: "allergies",  label: "Allergies" },
  { key: "docs",       label: "Documents" },
] as const;

type TabKey = typeof TABS[number]["key"];

export default function PatientDetailPage({ params }: { params: { id: string } }) {
  const id = Number(params.id);
  const [patient, setPatient] = useState<Patient | undefined>();
  const [measurements, setMeasurements] = useState<Measurement[]>([]);
  const [tab, setTab] = useState<TabKey>("overview");
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    getPatient(id).then(setPatient);
    getPatientMeasurements(id).then(setMeasurements);
  }, [id]);

  if (!patient) return <div className="p-6 text-sm text-slate-500">Loading…</div>;

  const enc = getCurrentEncounter(id);
  const diagnoses = getDiagnoses(id);
  const allergies = getAllergies(id);

  // simple vitals chart — synthesized series
  const chartData = id === 4
    ? [{x:"08:00",sys:158,hr:82},{x:"10:00",sys:160,hr:84},{x:"12:00",sys:162,hr:86},{x:"14:00",sys:162,hr:84},{x:"16:00",sys:160,hr:83}]
    : [{x:"08:00",sys:118,hr:76},{x:"10:00",sys:120,hr:78},{x:"12:00",sys:121,hr:80},{x:"14:00",sys:120,hr:78},{x:"16:00",sys:119,hr:77}];

  return (
    <div className="p-6 space-y-6">
      {/* breadcrumb */}
      <div className="flex items-center text-sm text-slate-500 gap-2">
        <Link href="/patients" className="hover:text-brand-600">Patients</Link>
        <ChevronRight className="w-3 h-3" />
        <span className="text-slate-900 font-medium">{patient.last}, {patient.first}</span>
      </div>

      {/* header card */}
      <div className="p-6 bg-white rounded-xl border border-slate-100 ring-soft">
        <div className="flex items-start justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className={cn("w-14 h-14 rounded-full grid place-items-center text-lg font-semibold", avatarColor(patient.id))}>
              {initials(patient)}
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-xl font-semibold text-slate-900">{patient.first} {patient.last}</h2>
                <StatusBadge status={patient.status} />
                {patient.alert && (
                  <span className="text-[11px] px-2 py-0.5 rounded-full bg-rose-100 text-rose-700 font-medium">
                    ⚠ {patient.alert}
                  </span>
                )}
              </div>
              <div className="text-sm text-slate-500 mt-1">
                MRN <span className="font-mono">{patient.mrn}</span> · {patient.sex} · {patient.age}y · DOB {patient.dob}
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            <button className="px-3 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center gap-2">
              <CalendarPlus className="w-4 h-4" /> Schedule
            </button>
            <button
              onClick={() => setModalOpen(true)}
              className="px-3 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center gap-2"
            >
              <Activity className="w-4 h-4" /> Record vitals
            </button>
            <button className="px-3 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700 flex items-center gap-2">
              <FilePlus className="w-4 h-4" /> New encounter
            </button>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-4 gap-4 text-sm">
          <div><div className="text-xs text-slate-500">Blood group</div><div className="font-medium">{patient.blood || "—"}</div></div>
          <div><div className="text-xs text-slate-500">Phone</div><div className="font-medium">{patient.phone || "—"}</div></div>
          <div><div className="text-xs text-slate-500">Insurance</div><div className="font-medium">{patient.ins || "—"}</div></div>
          <div><div className="text-xs text-slate-500">Primary care</div><div className="font-medium">{patient.pcp || "—"}</div></div>
        </div>
      </div>

      {/* tabs */}
      <div className="bg-white rounded-xl border border-slate-100 ring-soft">
        <div className="border-b border-slate-100 flex px-4">
          {TABS.map(t => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={cn(
                "px-4 py-3 text-sm font-medium border-b-2 transition",
                tab === t.key ? "text-brand-700 border-brand-600" : "text-slate-500 border-transparent hover:text-slate-700"
              )}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "overview" && (
          <div className="p-6 grid grid-cols-3 gap-6">
            <div className="col-span-2 space-y-5">
              <div>
                <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Current encounter</div>
                <div className="p-4 rounded-lg border border-slate-200">
                  {enc ? (
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-sm font-medium text-slate-900">{enc.num} · {enc.type}</div>
                        <div className="text-xs text-slate-500">{enc.date} · {enc.doctor}</div>
                        <div className="text-sm text-slate-700 mt-2">
                          <span className="text-xs text-slate-500">Chief complaint:</span> {enc.complaint}
                        </div>
                      </div>
                      <StatusBadge status={enc.status} />
                    </div>
                  ) : <div className="text-sm text-slate-500">No active encounter.</div>}
                </div>
              </div>
              <div>
                <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Recent vitals (last 24h)</div>
                <div className="h-48">
                  <ResponsiveContainer>
                    <LineChart data={chartData}>
                      <CartesianGrid stroke="#f1f5f9" vertical={false} />
                      <XAxis dataKey="x" stroke="#94a3b8" fontSize={11} />
                      <YAxis stroke="#94a3b8" fontSize={11} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: 11 }} />
                      <Line type="monotone" dataKey="sys" name="BP Systolic" stroke="#2563eb" strokeWidth={2} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="hr"  name="Heart Rate" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
            <div className="space-y-5">
              <div>
                <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Active diagnoses</div>
                <ul className="space-y-2 text-sm">
                  {diagnoses.length ? diagnoses.map((d, i) => (
                    <li key={i} className="flex items-center justify-between">
                      <span><span className="font-mono text-xs text-slate-500 mr-2">{d.code}</span>{d.text}</span>
                      <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{d.severity}</span>
                    </li>
                  )) : <li className="text-sm text-slate-500">None recorded.</li>}
                </ul>
              </div>
              <div>
                <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Allergies</div>
                <ul className="space-y-1 text-sm">
                  {allergies.length ? allergies.map((a, i) => <li key={i}>⚠️ {a}</li>) : <li className="text-sm text-slate-500">None recorded.</li>}
                </ul>
              </div>
            </div>
          </div>
        )}

        {tab === "vitals" && (
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-slate-900">Clinical measurements</div>
                <div className="text-xs text-slate-500">Unified (type · unit · value) per Appendix C.1</div>
              </div>
              <div className="flex gap-2">
                <a
                  href={exportMeasurementsUrl(patient.id, "csv")}
                  className="px-3 py-1.5 text-xs rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center gap-2"
                >
                  <Download className="w-3.5 h-3.5" /> Export CSV
                </a>
                <button
                  onClick={() => setModalOpen(true)}
                  className="px-3 py-1.5 text-xs rounded-lg bg-brand-600 text-white hover:bg-brand-700 flex items-center gap-2"
                >
                  <Plus className="w-3.5 h-3.5" /> Record
                </button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
                  <tr>
                    <th className="text-left px-4 py-2">Type</th>
                    <th className="text-left px-4 py-2">Value</th>
                    <th className="text-left px-4 py-2">Unit</th>
                    <th className="text-left px-4 py-2">Recorded by</th>
                    <th className="text-left px-4 py-2">Recorded at</th>
                    <th className="text-left px-4 py-2">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {measurements.length ? measurements.map((m, i) => (
                    <tr key={i} className="hover:bg-slate-50">
                      <td className="px-4 py-2 text-sm">{m.type}</td>
                      <td className="px-4 py-2 text-sm font-medium">{m.value}</td>
                      <td className="px-4 py-2 text-sm text-slate-500">{m.unit}</td>
                      <td className="px-4 py-2 text-sm text-slate-500">{m.by}</td>
                      <td className="px-4 py-2 text-sm text-slate-500">Today {m.at}</td>
                      <td className="px-4 py-2"><StatusBadge status={m.status} /></td>
                    </tr>
                  )) : (
                    <tr><td colSpan={6} className="px-4 py-6 text-center text-sm text-slate-500">No measurements recorded.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {tab === "encounters" && <div className="p-6 text-sm text-slate-500">Encounter history list (stub).</div>}
        {tab === "meds"       && <div className="p-6 text-sm text-slate-500">Active &amp; past prescriptions (stub).</div>}
        {tab === "allergies"  && <div className="p-6 text-sm text-slate-500">Allergy registry view (stub).</div>}
        {tab === "docs"       && <div className="p-6 text-sm text-slate-500">Uploaded documents (stub).</div>}
      </div>

      <RecordVitalsModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        patientLabel={`${patient.first} ${patient.last} · MRN ${patient.mrn}`}
        encounterNum={enc?.num || "ENC-NEW"}
        encounterId={1}
        onSaved={(rows) => setMeasurements((prev) => [...rows, ...prev])}
      />
    </div>
  );
}
