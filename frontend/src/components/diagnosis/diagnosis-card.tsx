"use client";

import { AlertTriangle, Stethoscope } from "lucide-react";

import { ConfidenceBadge } from "@/components/diagnosis/confidence-badge";
import { translate } from "@/lib/i18n";
import { confidenceTier } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";
import type { Diagnosis } from "@/types";

/**
 * A structured diagnosis card (PRD F3, RULE 306). Renders the assessed
 * problem, a three-tier confidence badge, and a prominent low-confidence
 * callout when the engine is unsure.
 */
export function DiagnosisCard({ diagnosis }: { diagnosis: Diagnosis }) {
  const language = useFarmStore((s) => s.language);
  const tier = confidenceTier(diagnosis.confidence);

  return (
    <section
      aria-label="Diagnosis"
      className="motion-safe:animate-[fade-in_var(--duration-normal)_var(--ease-out)] overflow-hidden rounded-lg border-l-2 border-accent bg-surface-elevated shadow-sm"
    >
      <div className="flex items-start justify-between gap-3 p-4">
        <div className="flex items-start gap-3">
          <div className="mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-md bg-accent-subtle text-accent">
            <Stethoscope className="size-5" aria-hidden />
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-text-tertiary">
              {translate(language, "diagnosis.title")}
            </p>
            <h3 className="text-lg font-semibold text-text-primary">
              {diagnosis.problem}
            </h3>
          </div>
        </div>
        <ConfidenceBadge confidence={diagnosis.confidence} />
      </div>

      {tier === "low" ? (
        <div
          role="note"
          className="flex items-start gap-2 border-t border-divider bg-error-subtle px-4 py-3 text-sm text-error"
        >
          <AlertTriangle className="mt-0.5 size-4 shrink-0" aria-hidden />
          <span>{translate(language, "confidence.lowCallout")}</span>
        </div>
      ) : null}
    </section>
  );
}
