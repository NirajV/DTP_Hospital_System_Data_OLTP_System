"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Users, Calendar, Stethoscope, FlaskConical,
  Pill, Receipt, BarChart3, ShieldCheck, Settings, ChevronDown,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/dashboard",    label: "Dashboard",    icon: LayoutDashboard },
  { href: "/patients",     label: "Patients",     icon: Users },
  { href: "/appointments", label: "Appointments", icon: Calendar },
  { href: "/encounters",   label: "Encounters",   icon: Stethoscope },
  { href: "/labs",         label: "Lab Orders",   icon: FlaskConical },
  { href: "/pharmacy",     label: "Pharmacy",     icon: Pill },
  { href: "/billing",      label: "Billing",      icon: Receipt },
  { href: "/reports",      label: "Reports",      icon: BarChart3 },
];

const SECONDARY = [
  { href: "/audit",    label: "Audit Trail", icon: ShieldCheck },
  { href: "/settings", label: "Settings",    icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const isActive = (href: string) => pathname === href || pathname?.startsWith(href + "/");

  return (
    <aside className="w-64 shrink-0 bg-white border-r border-slate-200 flex flex-col">
      <div className="h-16 px-5 flex items-center gap-3 border-b border-slate-200">
        <div className="w-9 h-9 rounded-lg bg-brand-600 grid place-items-center text-white font-bold">M</div>
        <div>
          <div className="font-semibold text-slate-900 leading-tight">MediFlow</div>
          <div className="text-[10px] uppercase tracking-wider text-slate-400">Riverside General</div>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-1 text-sm">
        {NAV.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-50 transition",
              isActive(href) && "bg-brand-50 text-brand-700"
            )}
          >
            <Icon className={cn("w-4 h-4", isActive(href) && "text-brand-700")} />
            {label}
          </Link>
        ))}

        <div className="pt-3 mt-3 border-t border-slate-100">
          {SECONDARY.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-50 transition",
                isActive(href) && "bg-brand-50 text-brand-700"
              )}
            >
              <Icon className={cn("w-4 h-4", isActive(href) && "text-brand-700")} />
              {label}
            </Link>
          ))}
        </div>
      </nav>

      <div className="p-3 border-t border-slate-200">
        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-50 cursor-pointer">
          <div className="w-9 h-9 rounded-full bg-emerald-100 text-emerald-700 grid place-items-center text-sm font-semibold">JS</div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-slate-900 truncate">Dr. Julia Smith</div>
            <div className="text-[11px] text-slate-500 truncate pulse-dot">Cardiology · On shift</div>
          </div>
          <ChevronDown className="w-4 h-4 text-slate-400" />
        </div>
      </div>
    </aside>
  );
}
