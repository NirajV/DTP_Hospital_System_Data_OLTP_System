"use client";

import Link from "next/link";
import { ENCOUNTERS_BOARD, PATIENTS } from "@/lib/mock-data";

function Card({ num, who, dr, t }: { num: string; who: string; dr: string; t: string }) {
  const p = PATIENTS.find((p) => `${p.first} ${p.last}` === who);
  const inner = (
    <div className="p-3 rounded-lg border border-slate-200 hover:bg-slate-50 cursor-pointer">
      <div className="flex items-center justify-between">
        <div className="text-sm font-medium text-slate-900">{who}</div>
        <div className="text-[11px] text-slate-500">{t}</div>
      </div>
      <div className="text-xs text-slate-500 mt-1">{num} · {dr}</div>
    </div>
  );
  return p ? <Link href={`/patients/${p.id}`}>{inner}</Link> : inner;
}

export default function EncountersPage() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Encounters</h1>
      <p className="text-sm text-slate-500">Active and recent encounters across the facility</p>

      <div className="grid grid-cols-3 gap-4">
        <Column title="In progress" items={ENCOUNTERS_BOARD.in_progress} />
        <Column title="Completed today" items={ENCOUNTERS_BOARD.completed} />
        <Column title="Scheduled" items={ENCOUNTERS_BOARD.scheduled} />
      </div>
    </div>
  );
}

function Column({ title, items }: { title: string; items: { num: string; who: string; dr: string; t: string }[] }) {
  return (
    <div className="p-4 bg-white rounded-xl border border-slate-100 ring-soft">
      <div className="text-xs uppercase text-slate-500 tracking-wider mb-2">{title}</div>
      <div className="space-y-2">
        {items.map((e) => <Card key={e.num} {...e} />)}
      </div>
    </div>
  );
}
