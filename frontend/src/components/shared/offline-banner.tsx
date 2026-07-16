"use client";

import { WifiOff } from "lucide-react";

import { useOnline } from "@/hooks/use-online";
import { translate } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";

/**
 * Persistent connectivity banner (PRD §13 network errors, RULE 503). Shown
 * only while offline; announced assertively for screen readers.
 */
export function OfflineBanner() {
  const online = useOnline();
  const language = useFarmStore((s) => s.language);

  if (online) return null;

  return (
    <div
      role="alert"
      className="flex items-center justify-center gap-2 bg-warning-subtle px-4 py-2 text-sm text-warning"
    >
      <WifiOff className="size-4 shrink-0" aria-hidden />
      <span>{translate(language, "common.offline")}</span>
    </div>
  );
}
