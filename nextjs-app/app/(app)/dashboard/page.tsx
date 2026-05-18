"use client";

import Link from "next/link";
import { Download, Plus, AlertCircle, AlertTriangle, Info } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell,
} from "recharts";
import { KpiCard } from "@/components/kpi-card";
import { StatusBadge } from "@/components/status-badge";
import {
  TODAY, ALERTS, WEEK_ENCOUNTERS, BED_OCCUPANCY, PATIENTS,
} from "@/lib/mock-data";

const PIE_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444"];

function alertIcon(sev: string) {
  if (sev === "high") return <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />;
  if (sev === "med")  return <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />;
  return <Info className="w-4 h-4 mt-0.5 shrink-0" />;
}

function alertPalette(sev: string) {
  if (sev === "high") return "bg-rose-50 text-rose-700 border-rose-100";
  if (sev === "med")  return "bg-amber-50 text-amber-700 border-amber-100";
  return "bg-slate-50 text-slate-700 border-slate-100";
}

export default function DashboardPage() {
  return (
    <div className="p-6 space-y-6">
      {/* greeting */}
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Good afternoon, Dr. Smith</h1>
          <p className="text-sm text-slate-500">Sunday, May 17, 2026 · 8 patients on your panel today</p>
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center gap-2">
            <Download className="w-4 h-4" /> Export day
          </button>
          <Link href="/encounters" className="px-3 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700 flex items-center gap-2">
            <Plus className="w-4 h-4" /> New encounter
          </Link>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-4 gap-4">
        <KpiCard label="Today's encounters" value={24} delta="+12%" hint="vs 21 yesterday" />
        <KpiCard label="Vitals recorded"    value={187} delta="+5%"  hint="measurements" />
        <KpiCard label="Abnormal results"   value={9}   delta="9 alerts" deltaTone="negative" hint="need review" />
        <KpiCard label="Avg encounter time" value={22}  unit="min" delta="last 7d" deltaTone="neutral" hint="target ≤ 25" />
      </div>

      {/* charts */}
      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2 p-5 bg-white rounded-xl border border-slate-100 ring-soft">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="font-semibold text-slate-900">Encounters this week</div>
              <div className="text-xs text-slate-500">Outpatient · Inpatient · Emergency</div>
            </div>
            <select className="text-xs border border-slate-200 rounded-md px-2 py-1">
              <option>Last 7 days</option>
              <option>Last 30 days</option>
            </select>
          </div>
          <div className="h-56">
            <ResponsiveContainer>
              <BarChart data={WEEK_ENCOUNTERS}>
                <CartesianGrid stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="outpatient" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                <Bar dataKey="inpatient"  fill="#10b981" radius={[6, 6, 0, 0]} />
                <Bar dataKey="emergency"  fill="#f59e0b" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-100 ring-soft">
          <div className="font-semibold text-slate-900 mb-1">Bed occupancy</div>
          <div className="text-xs text-slate-500 mb-4">By department</div>
          <div className="h-56">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={BED_OCCUPANCY} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius="55%" outerRadius="85%">
                  {BED_OCCUPANCY.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                </Pie>
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 10 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* today + alerts */}
      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2 p-5 bg-white rounded-xl border border-slate-100 ring-soft">
          <div className="flex items-center justify-between mb-4">
            <div className="font-semibold text-slate-900">Today's schedule</div>
            <Link href="/appointments" className="text-xs text-brand-600 hover:underline">View all</Link>
          </div>
          <div className="space-y-2">
            {TODAY.map((t) => {
              const p = PATIENTS.find(p => `${p.first} ${p.last}` === t.patient);
              const inner = (
                <div className="flex items-center gap-3 py-2 px-2 rounded-lg hover:bg-slate-50 cursor-pointer">
                  <div className="w-12 text-xs font-medium text-slate-500">{t.time}</div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-slate-900">{t.patient}</div>
                    <div className="text-xs text-slate-500">{t.reason} · {t.room}</div>
                  </div>
                  <StatusBadge status={t.status} />
                </div>
              );
              return p ? <Link key={t.time + t.patient} href={`/patients/${p.id}`}>{inner}</Link> : <div key={t.time + t.patient}>{inner}</div>;
            })}
          </div>
        </div>

        <div className="p-5 bg-white rounded-xl border border-slate-100 ring-soft">
          <div className="font-semibold text-slate-900 mb-4">Critical alerts</div>
          <div className="space-y-3">
            {ALERTS.map((a, i) => (
              <div key={i} className={`flex items-start gap-2 p-2 rounded-lg border ${alertPalette(a.sev)}`}>
                {alertIcon(a.sev)}
                <div className="text-xs">{a.text}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
