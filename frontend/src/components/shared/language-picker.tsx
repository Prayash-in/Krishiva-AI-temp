"use client";

import { Check } from "lucide-react";

import { LANGUAGES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import type { LanguageCode } from "@/types";

export interface LanguagePickerProps {
  value: LanguageCode;
  onChange: (code: LanguageCode) => void;
  /** "pills" for onboarding-style grid, "list" for settings rows. */
  variant?: "pills" | "list";
  className?: string;
}

/** The single language selector (PRD F8). Only engine-supported languages. */
export function LanguagePicker({
  value,
  onChange,
  variant = "pills",
  className,
}: LanguagePickerProps) {
  if (variant === "list") {
    return (
      <div className={cn("flex flex-col", className)} role="radiogroup">
        {LANGUAGES.map((lang) => {
          const selected = lang.code === value;
          return (
            <button
              key={lang.code}
              type="button"
              role="radio"
              aria-checked={selected}
              onClick={() => onChange(lang.code)}
              className={cn(
                "flex items-center justify-between border-b border-divider px-1 py-3 text-left",
                "transition-colors duration-[var(--duration-fast)] hover:bg-surface-hover",
              )}
            >
              <span className="text-base text-text-primary">
                {lang.label}
                <span className="ml-2 text-sm text-text-tertiary">
                  {lang.englishLabel}
                </span>
              </span>
              {selected ? (
                <Check className="size-5 text-accent" aria-hidden />
              ) : null}
            </button>
          );
        })}
      </div>
    );
  }

  return (
    <div
      className={cn("flex flex-wrap gap-2", className)}
      role="radiogroup"
      aria-label="Select language"
    >
      {LANGUAGES.map((lang) => {
        const selected = lang.code === value;
        return (
          <button
            key={lang.code}
            type="button"
            role="radio"
            aria-checked={selected}
            onClick={() => onChange(lang.code)}
            className={cn(
              "rounded-full border px-4 py-2 text-sm font-medium",
              "transition-colors duration-[var(--duration-fast)]",
              selected
                ? "border-accent bg-accent-subtle text-accent"
                : "border-border bg-surface-elevated text-text-secondary hover:bg-surface-hover",
            )}
          >
            {lang.label}
          </button>
        );
      })}
    </div>
  );
}
