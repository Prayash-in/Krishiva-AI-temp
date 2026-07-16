"use client";

import { AlertCircle, RotateCcw } from "lucide-react";

import { Button } from "@/components/ui";
import { translate } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";

/**
 * In-thread error card replacing a failed AI response (PRD §13 API errors).
 * Always specific and actionable — never a bare "something went wrong"
 * (RULE 500). Uses role="alert" for screen readers (RULE 505).
 */
export function ErrorCard({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  const language = useFarmStore((s) => s.language);

  return (
    <div
      role="alert"
      className="flex flex-col gap-3 rounded-lg border-l-2 border-error bg-error-subtle p-4"
    >
      <div className="flex items-start gap-2 text-error">
        <AlertCircle className="mt-0.5 size-5 shrink-0" aria-hidden />
        <p className="text-sm text-text-primary">{message}</p>
      </div>
      <div>
        <Button variant="secondary" size="sm" onClick={onRetry}>
          <RotateCcw className="size-4" aria-hidden />
          {translate(language, "chat.retry")}
        </Button>
      </div>
    </div>
  );
}
