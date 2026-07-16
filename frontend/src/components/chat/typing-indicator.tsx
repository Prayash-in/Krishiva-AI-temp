"use client";

import { useEffect, useState } from "react";

import { KrishivaLogo } from "@/components/icons/krishiva-logo";
import { translate } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";

/**
 * The "thinking" indicator (PRD §14.2). Three sequentially-pulsing dots in the
 * AI message slot. After 8s it appends a reassurance line. Since the MVP
 * backend is non-streaming, this shows for the whole request duration.
 */
export function TypingIndicator() {
  const language = useFarmStore((s) => s.language);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => window.clearInterval(id);
  }, []);

  return (
    <div className="flex items-start gap-3">
      <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-surface">
        <KrishivaLogo className="size-5" />
      </div>
      <div
        role="status"
        aria-label={translate(language, "chat.thinking")}
        className="rounded-lg rounded-tl-sm bg-surface-elevated px-4 py-3 shadow-sm"
      >
        <div className="flex items-center gap-1">
          <span className="size-2 rounded-full bg-text-tertiary motion-safe:animate-[dot-pulse_0.9s_infinite]" />
          <span className="size-2 rounded-full bg-text-tertiary motion-safe:animate-[dot-pulse_0.9s_infinite] [animation-delay:0.15s]" />
          <span className="size-2 rounded-full bg-text-tertiary motion-safe:animate-[dot-pulse_0.9s_infinite] [animation-delay:0.3s]" />
        </div>
        {elapsed >= 8 ? (
          <p className="mt-1.5 text-xs text-text-tertiary">
            {translate(language, "chat.stillWorking")}
          </p>
        ) : null}
      </div>
    </div>
  );
}
