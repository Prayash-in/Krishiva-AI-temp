"use client";

import { Circle, CircleDot, CircleDashed } from "lucide-react";

import { Badge, type BadgeTone } from "@/components/ui";
import { translate } from "@/lib/i18n";
import type { MessageKey } from "@/lib/i18n";
import { confidenceTier } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";
import type { ConfidenceTier } from "@/types";

const TIER: Record<
  ConfidenceTier,
  { tone: BadgeTone; icon: typeof Circle; labelKey: MessageKey }
> = {
  high: { tone: "success", icon: CircleDot, labelKey: "confidence.high" },
  medium: { tone: "warning", icon: CircleDashed, labelKey: "confidence.medium" },
  low: { tone: "error", icon: Circle, labelKey: "confidence.low" },
};

/**
 * Three-tier confidence indicator (PRD §14.6). Never shows the raw percentage
 * as the primary display; the exact value is only in the title tooltip.
 */
export function ConfidenceBadge({ confidence }: { confidence: number }) {
  const language = useFarmStore((s) => s.language);
  const tier = confidenceTier(confidence);
  const { tone, icon: Icon, labelKey } = TIER[tier];
  const pct = Math.round(confidence * 100);

  return (
    <Badge
      tone={tone}
      title={`Krishiva is ${pct}% confident in this diagnosis based on image analysis and knowledge base matching.`}
    >
      <Icon className="size-3" aria-hidden />
      {translate(language, labelKey)}
    </Badge>
  );
}
