"use client";

import { Sprout } from "lucide-react";

import { DiagnosisCard } from "@/components/diagnosis/diagnosis-card";
import { KrishivaLogo } from "@/components/icons/krishiva-logo";
import { ErrorCard } from "@/components/chat/error-card";
import { FeedbackButtons } from "@/components/chat/feedback-buttons";
import { MarkdownRenderer } from "@/components/chat/markdown-renderer";
import { SourcesDrawer } from "@/components/chat/sources-drawer";
import { Badge } from "@/components/ui";
import { translate } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";
import type { ChatMessage, FeedbackVote } from "@/types";

export interface MessageBubbleProps {
  message: ChatMessage;
  /** Whether this turn was answered with the farm profile as context. */
  hasFarmContext?: boolean;
  onRetry: () => void;
  onVote: (vote: FeedbackVote) => void;
}

/** Renders one turn — user (right) or assistant (left) — with rich cards (PRD F3). */
export function MessageBubble({
  message,
  hasFarmContext = false,
  onRetry,
  onVote,
}: MessageBubbleProps) {
  const language = useFarmStore((s) => s.language);

  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-lg rounded-tr-sm bg-accent-subtle px-4 py-2.5 text-base text-text-primary sm:max-w-[75%]">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="group flex items-start gap-3">
      <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-surface">
        <KrishivaLogo className="size-5" />
      </div>
      <div
        className="min-w-0 flex-1"
        aria-live="polite"
        aria-atomic="false"
      >
        {message.status === "error" ? (
          <ErrorCard
            message={message.errorMessage ?? translate(language, "error.generic")}
            onRetry={onRetry}
          />
        ) : (
          <div className="flex flex-col gap-3">
            {hasFarmContext ? (
              <Badge tone="accent" className="w-fit">
                <Sprout className="size-3" aria-hidden />
                {translate(language, "chat.contextBadge")}
              </Badge>
            ) : null}

            {message.diagnosis ? (
              <DiagnosisCard diagnosis={message.diagnosis} />
            ) : null}

            <MarkdownRenderer content={message.content} />

            <SourcesDrawer sources={message.sources ?? []} />

            <div className="pt-1">
              <FeedbackButtons value={message.feedback ?? null} onVote={onVote} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
