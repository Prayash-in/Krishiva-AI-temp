"use client";

import { Check } from "lucide-react";

import { COMMON_CROPS } from "@/lib/constants";
import { cn } from "@/lib/utils";

/** Multi-select chip selector for crops (PRD F9). */
export function CropSelector({
  selected,
  onToggle,
}: {
  selected: string[];
  onToggle: (crop: string) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label="Select crops">
      {COMMON_CROPS.map((crop) => {
        const active = selected.includes(crop);
        return (
          <button
            key={crop}
            type="button"
            aria-pressed={active}
            onClick={() => onToggle(crop)}
            className={cn(
              "inline-flex items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-sm font-medium",
              "transition-colors duration-[var(--duration-fast)]",
              active
                ? "border-accent bg-accent-subtle text-accent"
                : "border-border bg-surface-elevated text-text-secondary hover:bg-surface-hover",
            )}
          >
            {active ? <Check className="size-3.5" aria-hidden /> : null}
            {crop}
          </button>
        );
      })}
    </div>
  );
}
