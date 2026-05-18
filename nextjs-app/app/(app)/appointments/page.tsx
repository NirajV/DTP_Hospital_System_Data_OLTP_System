"use client";

import { CalendarPlus } from "lucide-react";

const HOURS = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"];
const DAYS = ["Sun 17", "Mon 18 · Today", "Tue 19", "Wed 20", "Thu 21", "Fri 22", "Sat 23"];

interface Appt { day: number; hour: string; label: string; cls: string }
const APPTS: Appt[] = [
  { day: 1, hour: "09:00", label: "M. Johnson · Follow-up", cls: "bg-blue-100 text-blue-800" },
  { day: 1, hour: "10:00", label: "A. Patel · Annual",      cls: "bg-emerald-100 text-emerald-800" },
  { day: 1, hour: "11:00", label: "D. Ramirez · BP check",  cls: "bg-amber-100 text-amber-800" },
  { day: 1, hour: "13:00", label: "S. Chen · Anaemia",      cls: "bg-violet-100 text-violet-800" },
  { day: 1, hour: "14:00", label: "L. Walsh · Knee pain",   cls: "bg-rose-100 text-rose-800" },
  { day: 1, hour: "15:00", label: "E. O’Brien · Vacc.",     cls: "bg-teal-100 text-teal-800" },
  { day: 3, hour: "10:00", label: "Y. Tanaka · CHF mgmt",   cls: "bg-blue-100 text-blue-800" },
  { day: 4, hour: "14:00", label: "N. Hassan · Endo",       cls: "bg-emerald-100 text-emerald-800" },
];

export default function AppointmentsPage() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Appointments</h1>
          <p className="text-sm text-slate-500">Week of May 17 – 23, 2026</p>
        </div>
        <div className="flex gap-2">
          <div className="flex border border-slate-200 rounded-lg overflow-hidden text-sm">
            <button className="px-3 py-1.5 bg-slate-100">Day</button>
            <button className="px-3 py-1.5 bg-white text-brand-700 font-medium">Week</button>
            <button className="px-3 py-1.5 bg-white">Month</button>
          </div>
          <button className="px-3 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700 flex items-center gap-2">
            <CalendarPlus className="w-4 h-4" /> New appointment
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-100 ring-soft overflow-hidden">
        <div className="grid grid-cols-8 text-xs font-medium text-slate-500 border-b border-slate-100">
          <div className="p-3">Time</div>
          {DAYS.map((d, i) => (
            <div key={d} className={`p-3 text-center ${i === 1 ? "bg-brand-50 text-brand-700" : ""}`}>
              {d}
            </div>
          ))}
        </div>
        {HOURS.map((h) => (
          <div key={h} className="grid grid-cols-8 border-b border-slate-100">
            <div className="p-2 text-xs text-slate-400 border-r border-slate-100">{h}</div>
            {Array.from({ length: 7 }).map((_, d) => {
              const a = APPTS.find((x) => x.day === d && x.hour === h);
              return (
                <div key={d} className="p-2 border-r border-slate-100 min-h-[44px]">
                  {a && (
                    <div className={`text-[11px] px-2 py-1 rounded ${a.cls} font-medium truncate`}>
                      {a.label}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
