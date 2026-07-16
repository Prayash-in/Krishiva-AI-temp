"use client";

import { ArrowUp, Camera, Mic, Square } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { IconButton } from "@/components/ui";
import { MAX_QUERY_LENGTH } from "@/lib/constants";
import { translate } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";

export interface ChatInputProps {
  onSend: (text: string) => void;
  onStop: () => void;
  isBusy: boolean;
  /** Controlled draft, so prompt suggestions can prefill it. */
  value: string;
  onChange: (value: string) => void;
}

/**
 * The anchored input bar (PRD P1). Auto-growing textarea, character guard,
 * send / stop toggle. Image and voice inputs are surfaced as disabled
 * affordances — the MVP engine accepts text only.
 */
export function ChatInput({
  onSend,
  onStop,
  isBusy,
  value,
  onChange,
}: ChatInputProps) {
  const language = useFarmStore((s) => s.language);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [shake, setShake] = useState(false);

  const trimmed = value.trim();
  const tooLong = value.length > MAX_QUERY_LENGTH;
  const nearLimit = value.length > MAX_QUERY_LENGTH * 0.9;
  const canSend = trimmed.length > 0 && !tooLong && !isBusy;

  // Auto-resize the textarea to fit content (capped).
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [value]);

  const submit = () => {
    if (!canSend) {
      if (trimmed.length === 0) {
        setShake(true);
        window.setTimeout(() => setShake(false), 200);
        textareaRef.current?.focus();
      }
      return;
    }
    onSend(trimmed);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div className="mx-auto w-full max-w-3xl px-3 pb-3 sm:px-4 sm:pb-4">
      <div
        className={cn(
          "flex items-end gap-1.5 rounded-2xl border border-border bg-surface-elevated p-1.5 shadow-md",
          "transition-colors duration-[var(--duration-fast)] focus-within:border-border-strong",
          tooLong && "border-error",
          shake && "motion-safe:animate-[shake_0.2s]",
        )}
      >
        <IconButton
          label="Add a photo (coming soon)"
          title="Photo diagnosis is coming soon"
          disabled
        >
          <Camera className="size-5" aria-hidden />
        </IconButton>

        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder={translate(language, "chat.placeholder")}
          aria-label={translate(language, "chat.placeholder")}
          className={cn(
            "max-h-[200px] min-h-[2.75rem] flex-1 resize-none bg-transparent px-2 py-2.5",
            "text-base text-text-primary placeholder:text-text-tertiary focus:outline-none",
          )}
        />

        <IconButton
          label="Voice input (coming soon)"
          title="Voice input is coming soon"
          disabled
        >
          <Mic className="size-5" aria-hidden />
        </IconButton>

        {isBusy ? (
          <IconButton
            label={translate(language, "chat.stop")}
            onClick={onStop}
            className="bg-surface-active text-text-primary"
          >
            <Square className="size-4 fill-current" aria-hidden />
          </IconButton>
        ) : (
          <IconButton
            label={translate(language, "chat.send")}
            onClick={submit}
            disabled={!canSend}
            className={cn(
              canSend && "bg-accent text-text-inverse hover:enabled:bg-accent-hover hover:enabled:text-text-inverse",
            )}
          >
            <ArrowUp className="size-5" aria-hidden />
          </IconButton>
        )}
      </div>

      {nearLimit ? (
        <p
          className={cn(
            "mt-1 px-2 text-right text-xs",
            tooLong ? "text-error" : "text-text-tertiary",
          )}
        >
          {value.length.toLocaleString()} / {MAX_QUERY_LENGTH.toLocaleString()}
        </p>
      ) : null}
    </div>
  );
}
