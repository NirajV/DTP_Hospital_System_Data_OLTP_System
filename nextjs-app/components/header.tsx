"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Search, Bell, HelpCircle, LogOut } from "lucide-react";
import { searchPatients } from "@/lib/api";
import type { SearchResult } from "@/lib/types";
import { cn } from "@/lib/utils";

export function Header() {
  const router = useRouter();
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const boxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const t = setTimeout(async () => {
      if (!q.trim()) { setResults([]); setOpen(false); return; }
      const items = await searchPatients(q.trim());
      setResults(items);
      setOpen(true);
    }, 150);
    return () => clearTimeout(t);
  }, [q]);

  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (!boxRef.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  function logout() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_role");
    }
    router.push("/login");
  }

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center px-6 gap-4">
      <div ref={boxRef} className="flex-1 max-w-xl relative">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onFocus={() => results.length && setOpen(true)}
          placeholder="Search patients by MRN, name, or DOB…"
          className="w-full pl-9 pr-3 py-2 rounded-lg bg-slate-50 border border-transparent focus:bg-white focus:border-slate-200 focus:ring-2 focus:ring-brand-100 outline-none text-sm"
        />
        {open && (
          <div className="absolute z-30 mt-1 w-full bg-white rounded-lg ring-soft border border-slate-100 max-h-72 overflow-auto">
            {results.length ? results.map((r) => (
              <Link
                key={`${r.type}-${r.id}`}
                href={r.url.startsWith("/api") ? `/patients/${r.id}` : r.url}
                onClick={() => { setOpen(false); setQ(""); }}
                className="block px-4 py-2 hover:bg-slate-50 text-sm"
              >
                <div className="font-medium text-slate-900">{r.label}</div>
                {r.snippet && <div className="text-xs text-slate-500">{r.snippet}</div>}
              </Link>
            )) : (
              <div className="px-4 py-3 text-sm text-slate-500">No matches.</div>
            )}
          </div>
        )}
      </div>

      <button className={cn("relative p-2 rounded-lg hover:bg-slate-100")}>
        <Bell className="w-5 h-5 text-slate-600" />
        <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500" />
      </button>
      <button className="p-2 rounded-lg hover:bg-slate-100">
        <HelpCircle className="w-5 h-5 text-slate-600" />
      </button>
      <div className="h-8 w-px bg-slate-200" />
      <button
        onClick={logout}
        className="text-sm text-slate-600 hover:text-slate-900 flex items-center gap-2"
      >
        <LogOut className="w-4 h-4" /> Sign out
      </button>
    </header>
  );
}
