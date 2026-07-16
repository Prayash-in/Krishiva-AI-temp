"use client";

import { BookOpen, ChevronDown } from "lucide-react";
import { useId, useState } from "react";

import { translate } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";
import type { Source } from "@/types";

/**
 * Expandable citation drawer (PRD §14.5, RULE 307). Expands inline below the
 * response — not a modal. The MVP engine returns knowledge-base chunks
 * (`id`, `title`, `score`) with no external URL, so we cite the KB entry and
 * its relevance without fabricating links (PRD §14.1 "no hallucinated links").
 */
export function SourcesDrawer({ sources }: { sources: Source[] }) {
  const language = useFarmStore((s) => s.language);
  const [open, setOpen] = useState(false);
  const panelId = useId();

  if (sources.length === 0) {
    return (
      <p className="mt-2 text-xs text-text-tertiary">
        {translate(language, "chat.generalGuidance")}
      </p>
    );
  }

  return (
    <div className="mt-3">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls={panelId}
        className={cn(
          "inline-flex items-center gap-1.5 rounded-full bg-accent-subtle px-3 py-1 text-xs font-medium text-accent",
          "transition-colors duration-[var(--duration-fast)] hover:bg-surface-hover",
        )}
      >
        <BookOpen className="size-3.5" aria-hidden />
        {translate(language, "chat.sources")} · {sources.length}
        <ChevronDown
          className={cn(
            "size-3.5 transition-transform duration-[var(--duration-fast)]",
            open && "rotate-180",
          )}
          aria-hidden
        />
      </button>

      {open ? (
        <ol
          id={panelId}
          className="motion-safe:animate-[fade-in_var(--duration-normal)_var(--ease-out)] mt-2 flex flex-col gap-2"
        >
          {sources.map((source, index) => (
            <li
              key={source.id}
              className="flex items-start gap-2 rounded-md border border-border bg-surface-elevated p-3"
            >
              <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full bg-accent-subtle text-[10px] font-semibold text-accent">
                {index + 1}
              </span>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-text-primary">
                  {source.title}
                </p>
                <p className="text-xs text-text-tertiary">
                  📚 Knowledge base
                  {typeof source.score === "number"
                    ? ` · ${Math.round(source.score * 100)}% match`
                    : ""}
                </p>
              </div>
            </li>
          ))}
        </ol>
      ) : null}
    </div>
  );
}
