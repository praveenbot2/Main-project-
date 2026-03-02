import clsx from "clsx";
import { AlertTriangle, CheckCircle, AlertCircle } from "lucide-react";
import type { RiskLevel } from "@/lib/types";

interface RiskBannerProps {
  riskLevel: RiskLevel;
  probability: number;
  message?: string;
}

const CONFIG: Record<
  RiskLevel,
  { bg: string; border: string; text: string; Icon: typeof AlertTriangle }
> = {
  High: {
    bg: "bg-red-950/40",
    border: "border-red-500/50",
    text: "text-red-300",
    Icon: AlertCircle,
  },
  Medium: {
    bg: "bg-amber-950/40",
    border: "border-amber-500/50",
    text: "text-amber-300",
    Icon: AlertTriangle,
  },
  Low: {
    bg: "bg-emerald-950/40",
    border: "border-emerald-500/50",
    text: "text-emerald-300",
    Icon: CheckCircle,
  },
};

export default function RiskBanner({
  riskLevel,
  probability,
  message,
}: RiskBannerProps) {
  const { bg, border, text, Icon } = CONFIG[riskLevel];

  return (
    <div
      className={clsx(
        "flex items-start gap-3 rounded-xl border-l-4 p-4",
        bg,
        border,
      )}
    >
      <Icon className={clsx("mt-0.5 h-5 w-5 shrink-0", text)} />
      <div>
        <p className={clsx("font-semibold", text)}>
          {riskLevel} Risk&nbsp;
          <span className="font-normal">
            ({(probability * 100).toFixed(1)}%)
          </span>
        </p>
        {message && <p className={clsx("mt-1 text-sm", text)}>{message}</p>}
      </div>
    </div>
  );
}
