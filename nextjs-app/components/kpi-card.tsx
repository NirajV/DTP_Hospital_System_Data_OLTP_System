export function KpiCard({
  label,
  value,
  unit,
  delta,
  deltaTone = "positive",
  hint,
}: {
  label: string;
  value: string | number;
  unit?: string;
  delta?: string;
  deltaTone?: "positive" | "negative" | "neutral";
  hint?: string;
}) {
  const deltaColor =
    deltaTone === "positive" ? "text-emerald-600"
    : deltaTone === "negative" ? "text-rose-600"
    : "text-slate-400";

  return (
    <div className="p-5 bg-white rounded-xl border border-slate-100 ring-soft">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">{label}</span>
        {delta && <span className={`${deltaColor} text-xs font-medium`}>{delta}</span>}
      </div>
      <div className="mt-2 flex items-end gap-2">
        <div className="text-3xl font-semibold text-slate-900">
          {value}
          {unit && <span className="text-base text-slate-400 ml-0.5">{unit}</span>}
        </div>
        {hint && <div className="text-xs text-slate-500 mb-1">{hint}</div>}
      </div>
    </div>
  );
}
