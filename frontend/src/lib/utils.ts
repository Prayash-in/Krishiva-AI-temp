import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

import type { ConfidenceTier } from "@/types";

/** Merge conditional class names, de-duplicating conflicting Tailwind utilities. */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/** Map an engine confidence score (0–1) to the three-tier system (PRD §14.6). */
export function confidenceTier(confidence: number): ConfidenceTier {
  if (confidence >= 0.85) return "high";
  if (confidence >= 0.6) return "medium";
  return "low";
}

/** A short, stable-ish id for client-only entities. */
export function makeId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

/** Derive a conversation title from the first user message. */
export function deriveTitle(text: string): string {
  const trimmed = text.trim().replace(/\s+/g, " ");
  if (trimmed.length <= 48) return trimmed;
  return `${trimmed.slice(0, 47)}…`;
}

/** Human-friendly relative day grouping label for history. */
export function relativeDay(timestamp: number): string {
  const now = new Date();
  const then = new Date(timestamp);
  const startOfDay = (d: Date) =>
    new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
  const diffDays = Math.round(
    (startOfDay(now) - startOfDay(then)) / 86_400_000,
  );
  if (diffDays <= 0) return "Today";
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return "This week";
  if (diffDays < 30) return "This month";
  return "Earlier";
}
