import { forwardRef, type HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export type BadgeTone =
  | "neutral"
  | "accent"
  | "success"
  | "warning"
  | "error"
  | "info";

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: BadgeTone;
}

const TONES: Record<BadgeTone, string> = {
  neutral: "bg-surface-inset text-text-secondary",
  accent: "bg-accent-subtle text-accent",
  success: "bg-success-subtle text-success",
  warning: "bg-warning-subtle text-warning",
  error: "bg-error-subtle text-error",
  info: "bg-info-subtle text-info",
};

/** A small status/label pill. Variants via `tone` (PRD §16.1). */
export const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, tone = "neutral", ...props }, ref) => (
    <span
      ref={ref}
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium",
        TONES[tone],
        className,
      )}
      {...props}
    />
  ),
);
Badge.displayName = "Badge";
