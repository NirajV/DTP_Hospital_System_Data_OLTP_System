"use client";

import { Activity, Users, Stethoscope, Receipt, ShieldAlert, FileText, Download, Plus } from "lucide-react";
import type { ComponentType, SVGProps } from "react";
import { exportMeasurementsUrl } from "@/lib/api";

interface ReportCard {
  icon: ComponentType<SVGProps<SVGSVGElement>>;
  tone: string;
  title: string;
  desc: string;
  cta: string;
  href?: string;
  ctaIcon: ComponentType<SVGProps<SVGSVGElement>>;
}

const REPORTS: ReportCard[] = [
  {
    icon: Activity, tone: "text-brand-600",
    title: "Patient vitals export",
    desc: "CSV / Excel · 90-day window · all measurement types",
    cta: "Generate",
    href: exportMeasurementsUrl(1, "csv"),
    ctaIcon: Download,
  },
  {
    icon: Users, tone: "text-emerald-600",
    title: "Daily census",
    desc: "PDF · admissions, discharges, bed occupancy",
    cta: "Generate", ctaIcon: Download,
  },
  {
    icon: Stethoscope, tone: "text-violet-600",
    title: "Doctor performance",
    desc: "Excel · 90-day · encounters, avg time, outcomes",
    cta: "Generate", ctaIcon: Download,
  },
  {
    icon: Receipt, tone: "text-amber-600",
    title: "A/R aging",
    desc: "Excel · outstanding invoices by bucket",
    cta: "Generate", ctaIcon: Download,
  },
  {
    icon: ShieldAlert, tone: "text-rose-600",
    title: "Credential expiry",
    desc: "CSV · clinicians with licenses expiring ≤ 60 days",
    cta: "Generate", ctaIcon: Download,
  },
  {
    icon: FileText, tone: "text-slate-600",
    title: "Custom query",
    desc: "Build your own report using saved views",
    cta: "New report", ctaIcon: Plus,
  },
];

export default function ReportsPage() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Reports &amp; Export</h1>
          <p className="text-sm text-slate-500">Per Appendix C.3 — exports audited; PHI restricted by role</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {REPORTS.map((r) => {
          const Icon = r.icon;
          const CtaIcon = r.ctaIcon;
          const cta = (
            <button className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 hover:bg-slate-50 flex items-center justify-center gap-2">
              <CtaIcon className="w-4 h-4" /> {r.cta}
            </button>
          );
          return (
            <div key={r.title} className="p-5 bg-white rounded-xl border border-slate-100 ring-soft">
              <div className="flex items-center gap-3 mb-2">
                <Icon className={`w-5 h-5 ${r.tone}`} />
                <div className="font-medium">{r.title}</div>
              </div>
              <p className="text-xs text-slate-500 mb-3">{r.desc}</p>
              {r.href ? <a href={r.href} target="_blank" rel="noopener noreferrer">{cta}</a> : cta}
            </div>
          );
        })}
      </div>
    </div>
  );
}
