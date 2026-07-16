"use client";

import { ThumbsDown, ThumbsUp } from "lucide-react";

import { IconButton } from "@/components/ui";
import { translate } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";
import type { FeedbackVote } from "@/types";

export interface FeedbackButtonsProps {
  value: FeedbackVote;
  onVote: (vote: FeedbackVote) => void;
}

/** Thumbs up/down on each AI response (PRD F23). Toggles off when re-pressed. */
export function FeedbackButtons({ value, onVote }: FeedbackButtonsProps) {
  const language = useFarmStore((s) => s.language);

  const toggle = (vote: Exclude<FeedbackVote, null>) =>
    onVote(value === vote ? null : vote);

  return (
    <div
      className="flex items-center gap-0.5"
      role="group"
      aria-label="Rate this response"
    >
      <IconButton
        label={translate(language, "feedback.up")}
        size="sm"
        active={value === "up"}
        onClick={() => toggle("up")}
      >
        <ThumbsUp className="size-4" aria-hidden />
      </IconButton>
      <IconButton
        label={translate(language, "feedback.down")}
        size="sm"
        active={value === "down"}
        onClick={() => toggle("down")}
      >
        <ThumbsDown className="size-4" aria-hidden />
      </IconButton>
    </div>
  );
}
