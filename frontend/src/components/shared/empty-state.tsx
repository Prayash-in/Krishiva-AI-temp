import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  subtext: string;
  action?: ReactNode;
  className?: string;
}

/**
 * The single empty-state pattern (PRD §12). Monoline icon, headline, subtext,
 * optional CTA — vertically centered in the available space.
 */
export function EmptyState({
  icon: Icon,
  title,
  subtext,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center px-6 text-center",
        "motion-safe:animate-[fade-in_var(--duration-moderate)_var(--ease-out)]",
        className,
      )}
    >
      <div className="mb-5 flex size-20 items-center justify-center rounded-2xl bg-surface text-text-tertiary">
        <Icon strokeWidth={1.5} className="size-9" aria-hidden />
      </div>
      <h2 className="text-xl font-semibold text-text-primary">{title}</h2>
      <p className="mt-2 max-w-sm text-sm text-text-secondary">{subtext}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}
