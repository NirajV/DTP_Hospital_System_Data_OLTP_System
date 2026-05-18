"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Search, Filter, Download, UserPlus, ChevronRight } from "lucide-react";
import { listPatients } from "@/lib/api";
import { StatusBadge } from "@/components/status-badge";
import { NewPatientModal } from "@/components/new-patient-modal";
import { initials, avatarColor, cn } from "@/lib/utils";
import type { Patient } from "@/lib/types";

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [filter, setFilter] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  useEffect(() => { listPatients().then(setPatients); }, []);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 2800);
    return () => clearTimeout(t);
  }, [toast]);

  const rows = useMemo(() => {
    const f = filter.trim().toLowerCase();
    if (!f) return patients;
    return patients.filter(p =>
      p.first.toLowerCase().includes(f) ||
      p.last.toLowerCase().includes(f) ||
      p.mrn.toLowerCase().includes(f)
    );
  }, [patients, filter]);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Patients</h1>
          <p className="text-sm text-slate-500">All active patients in your facility</p>
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center gap-2">
            <Filter className="w-4 h-4" /> Filters
          </button>
          <button className="px-3 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center gap-2">
            <Download className="w-4 h-4" /> Export
          </button>
          <button
            onClick={() => setModalOpen(true)}
            className="px-3 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700 flex items-center gap-2"
          >
            <UserPlus className="w-4 h-4" /> New patient
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-100 ring-soft overflow-hidden">
        <div className="px-5 py-3 border-b border-slate-100 flex items-center gap-3">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              placeholder="Filter patients…"
              className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-slate-50 border border-transparent focus:bg-white focus:border-slate-200 outline-none text-sm"
            />
          </div>
          <select className="text-xs border border-slate-200 rounded-md px-2 py-1.5">
            <option>All status</option><option>Active</option><option>Inactive</option>
          </select>
          <select className="text-xs border border-slate-200 rounded-md px-2 py-1.5">
            <option>All departments</option><option>Cardiology</option><option>Oncology</option>
          </select>
        </div>

        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
            <tr>
              <th className="text-left px-5 py-3">Patient</th>
              <th className="text-left px-5 py-3">MRN</th>
              <th className="text-left px-5 py-3">DOB / Age</th>
              <th className="text-left px-5 py-3">Last visit</th>
              <th className="text-left px-5 py-3">Primary doctor</th>
              <th className="text-left px-5 py-3">Status</th>
              <th className="px-5 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((p) => (
              <tr key={p.id} className="hover:bg-slate-50">
                <td className="px-5 py-3">
                  <Link href={`/patients/${p.id}`} className="flex items-center gap-3">
                    <div className={cn("w-9 h-9 rounded-full grid place-items-center text-xs font-semibold", avatarColor(p.id))}>
                      {initials(p)}
                    </div>
                    <div>
                      <div className="font-medium text-slate-900">{p.last}, {p.first}</div>
                      <div className="text-xs text-slate-500">{p.sex} · {p.age}y</div>
                    </div>
                  </Link>
                </td>
                <td className="px-5 py-3 font-mono text-xs">{p.mrn}</td>
                <td className="px-5 py-3 text-sm">{p.dob}</td>
                <td className="px-5 py-3 text-sm">{p.id === 1 || p.id === 4 ? "Today" : "2 weeks ago"}</td>
                <td className="px-5 py-3 text-sm">{p.pcp}</td>
                <td className="px-5 py-3"><StatusBadge status={p.status} /></td>
                <td className="px-5 py-3 text-right">
                  <Link href={`/patients/${p.id}`}>
                    <ChevronRight className="w-4 h-4 text-slate-400 inline" />
                  </Link>
                </td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr><td colSpan={7} className="px-5 py-10 text-center text-sm text-slate-500">No patients match.</td></tr>
            )}
          </tbody>
        </table>

        <div className="px-5 py-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <div>Showing 1 – {rows.length} of {patients.length} patients</div>
          <div className="flex items-center gap-1">
            <button className="px-2 py-1 rounded border border-slate-200 hover:bg-slate-50">←</button>
            <button className="px-2 py-1 rounded border border-brand-600 bg-brand-50 text-brand-700">1</button>
            <button className="px-2 py-1 rounded border border-slate-200 hover:bg-slate-50">2</button>
            <button className="px-2 py-1 rounded border border-slate-200 hover:bg-slate-50">3</button>
            <button className="px-2 py-1 rounded border border-slate-200 hover:bg-slate-50">→</button>
          </div>
        </div>
      </div>

      <NewPatientModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onCreated={(p) => {
          setPatients((prev) => [p, ...prev]);
          setToast(`✓ Patient ${p.first} ${p.last} created · MRN ${p.mrn}`);
        }}
      />

      {toast && (
        <div className="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-lg bg-slate-900 text-white text-sm ring-soft">
          {toast}
        </div>
      )}
    </div>
  );
}
