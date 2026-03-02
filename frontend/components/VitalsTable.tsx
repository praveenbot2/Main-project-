import type { Vitals } from "@/lib/types";
import clsx from "clsx";

interface VitalsTableProps {
  vitals: Vitals;
}

const ROWS: {
  key: keyof Vitals;
  label: string;
  unit: string;
  normal: [number, number];
}[] = [
  { key: "heart_rate", label: "Heart Rate", unit: "bpm", normal: [60, 100] },
  {
    key: "blood_pressure_systolic",
    label: "BP Systolic",
    unit: "mmHg",
    normal: [90, 120],
  },
  {
    key: "blood_pressure_diastolic",
    label: "BP Diastolic",
    unit: "mmHg",
    normal: [60, 80],
  },
  {
    key: "temperature",
    label: "Temperature",
    unit: "°C",
    normal: [36.1, 37.2],
  },
  { key: "oxygen_saturation", label: "SpO₂", unit: "%", normal: [95, 100] },
  {
    key: "respiratory_rate",
    label: "Resp. Rate",
    unit: "br/min",
    normal: [12, 20],
  },
];

function inRange(val: number, [lo, hi]: [number, number]) {
  return val >= lo && val <= hi;
}

export default function VitalsTable({ vitals }: VitalsTableProps) {
  return (
    <div className="overflow-hidden rounded-xl border border-white/[0.08]">
      <table className="min-w-full text-sm">
        <thead className="bg-white/[0.04] text-left text-xs font-semibold uppercase tracking-wide text-teal-300/70">
          <tr>
            <th className="px-4 py-3">Vital</th>
            <th className="px-4 py-3">Value</th>
            <th className="px-4 py-3">Normal Range</th>
            <th className="px-4 py-3">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/[0.06]">
          {ROWS.map(({ key, label, unit, normal }) => {
            const val = vitals[key];
            const ok = inRange(val, normal);
            return (
              <tr key={key} className="hover:bg-white/[0.03] transition-colors">
                <td className="px-4 py-3 font-medium text-white/80">{label}</td>
                <td className="px-4 py-3 text-white/70">
                  {typeof val === "number" ? val.toFixed(1) : val} {unit}
                </td>
                <td className="px-4 py-3 text-white/40">
                  {normal[0]}–{normal[1]} {unit}
                </td>
                <td className="px-4 py-3">
                  <span
                    className={clsx(
                      "inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold",
                      ok
                        ? "bg-emerald-900/50 text-emerald-300"
                        : "bg-red-900/50 text-red-300",
                    )}
                  >
                    {ok ? "Normal" : "Abnormal"}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
