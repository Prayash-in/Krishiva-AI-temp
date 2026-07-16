"use client";

import { ArrowUpRight } from "lucide-react";

import { PROMPT_SUGGESTIONS } from "@/lib/constants";
import { cn } from "@/lib/utils";

/**
 * Suggested prompt cards for the empty state (PRD F4). Tapping one submits it
 * immediately.
 */
export function PromptSuggestions({
  onSelect,
  className,
}: {
  onSelect: (prompt: string) => void;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "grid w-full max-w-xl grid-cols-1 gap-2 sm:grid-cols-2",
        className,
      )}
    >
      {PROMPT_SUGGESTIONS.map((prompt) => (
        <button
          key={prompt}
          type="button"
          onClick={() => onSelect(prompt)}
          className={cn(
            "group flex items-center justify-between gap-2 rounded-lg border border-border bg-surface-elevated px-4 py-3 text-left",
            "text-sm text-text-primary shadow-sm transition-colors duration-[var(--duration-fast)]",
            "hover:border-border-strong hover:bg-surface-hover",
          )}
        >
          <span>{prompt}</span>
          <ArrowUpRight
            className="size-4 shrink-0 text-text-tertiary transition-colors group-hover:text-accent"
            aria-hidden
          />
        </button>
      ))}
    </div>
  );
}
