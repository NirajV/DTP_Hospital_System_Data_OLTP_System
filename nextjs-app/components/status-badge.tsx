import { cn } from "@/lib/utils";

type StatusKey =
  | "completed" | "in_progress" | "scheduled" | "cancelled"
  | "active" | "inactive"
  | "Normal" | "High" | "Low";

const MAP: Record<StatusKey, { cls: string; label: string }> = {
  completed:   { cls: "bg-emerald-50 text-emerald-700", label: "Completed" },
  in_progress: { cls: "bg-blue-50 text-blue-700",       label: "In progress" },
  scheduled:   { cls: "bg-slate-100 text-slate-600",    label: "Scheduled" },
  cancelled:   { cls: "bg-rose-50 text-rose-700",       label: "Cancelled" },
  active:      { cls: "bg-emerald-50 text-emerald-700", label: "Active" },
  inactive:    { cls: "bg-slate-100 text-slate-500",    label: "Inactive" },
  Normal:      { cls: "bg-emerald-50 text-emerald-700", label: "Normal" },
  High:        { cls: "bg-rose-50 text-rose-700",       label: "High" },
  Low:         { cls: "bg-amber-50 text-amber-700",     label: "Low" },
};

export function StatusBadge({ status, className }: { status: string; className?: string }) {
  const entry = MAP[status as StatusKey] ?? { cls: "bg-slate-100 text-slate-600", label: status };
  return (
    <span className={cn("text-[11px] px-2 py-0.5 rounded-full font-medium", entry.cls, className)}>
      {entry.label}
    </span>
  );
}
