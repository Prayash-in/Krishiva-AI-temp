"use client";

import { ArrowDown } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { ChatInput } from "@/components/chat/chat-input";
import { MessageBubble } from "@/components/chat/message-bubble";
import { PromptSuggestions } from "@/components/chat/prompt-suggestions";
import { TypedBrand } from "@/components/chat/typed-brand";
import { TypingIndicator } from "@/components/chat/typing-indicator";
import { KrishivaLogo } from "@/components/icons/krishiva-logo";
import { LanguagePicker } from "@/components/shared/language-picker";
import { useChat } from "@/hooks/use-chat";
import { useMounted } from "@/hooks/use-mounted";
import { translate } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";

/**
 * The chat surface (PRD P1). Empty state with greeting + prompts, or the
 * scrollable thread. Auto-scrolls while answering unless the user scrolls up,
 * then offers a "new content" pill (RULE 304).
 */
export function ChatView({ conversationId }: { conversationId?: string }) {
  const mounted = useMounted();
  const language = useFarmStore((s) => s.language);
  const setLanguage = useFarmStore((s) => s.setLanguage);
  const {
    messages,
    isBusy,
    hasFarmContext,
    send,
    stop,
    retry,
    setFeedback,
  } = useChat(conversationId);

  const [draft, setDraft] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  const [pinned, setPinned] = useState(true);

  const scrollToBottom = useCallback((behavior: ScrollBehavior = "smooth") => {
    const el = scrollRef.current;
    if (el) el.scrollTo({ top: el.scrollHeight, behavior });
  }, []);

  const onScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    const distance = el.scrollHeight - el.scrollTop - el.clientHeight;
    setPinned(distance < 80);
  }, []);

  // Keep the latest content in view while pinned.
  useEffect(() => {
    if (pinned) scrollToBottom(messages.length <= 1 ? "auto" : "smooth");
  }, [messages, isBusy, pinned, scrollToBottom]);

  const handleSend = (text: string) => {
    setDraft("");
    setPinned(true);
    send(text);
  };

  const isEmpty = mounted && messages.length === 0;

  return (
    <div className="flex h-full flex-col">
      <div
        ref={scrollRef}
        onScroll={onScroll}
        className="relative min-h-0 flex-1 overflow-y-auto"
      >
        {isEmpty ? (
          <div className="mx-auto flex h-full max-w-2xl flex-col items-center justify-center gap-8 px-4 py-8 text-center">
            <KrishivaLogo
              title="Krishiva"
              className="size-16 drop-shadow-sm motion-safe:animate-[leaf-float_3.5s_ease-in-out_infinite] sm:size-20"
            />
            <div className="flex flex-col items-center gap-3">
              <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-4xl font-semibold tracking-tight sm:text-5xl">
                <span className="text-text-secondary">
                  {translate(language, "chat.greeting")}
                </span>
                <TypedBrand className="inline-flex min-h-[1.25em] items-center text-text-primary" />
              </div>
              <p className="max-w-md text-sm text-text-secondary">
                {translate(language, "chat.subgreeting")}
              </p>
            </div>
            <PromptSuggestions onSelect={handleSend} />
            <LanguagePicker value={language} onChange={setLanguage} />
          </div>
        ) : (
          <div className="mx-auto flex max-w-3xl flex-col gap-6 px-3 py-6 sm:px-4">
            {messages.map((message) =>
              message.role === "assistant" && message.status === "thinking" ? (
                <TypingIndicator key={message.id} />
              ) : (
                <MessageBubble
                  key={message.id}
                  message={message}
                  hasFarmContext={hasFarmContext && !!message.diagnosis}
                  onRetry={() => retry(message.id)}
                  onVote={(vote) => setFeedback(message.id, vote)}
                />
              ),
            )}
          </div>
        )}

        {!pinned ? (
          <button
            type="button"
            onClick={() => {
              setPinned(true);
              scrollToBottom();
            }}
            className={cn(
              "sticky bottom-4 left-1/2 flex -translate-x-1/2 items-center gap-1.5 rounded-full",
              "border border-border bg-surface-elevated px-3 py-1.5 text-xs font-medium text-text-primary shadow-md",
            )}
          >
            <ArrowDown className="size-3.5" aria-hidden />
            {translate(language, "chat.newContent")}
          </button>
        ) : null}
      </div>

      <ChatInput
        value={draft}
        onChange={setDraft}
        onSend={handleSend}
        onStop={stop}
        isBusy={isBusy}
      />
    </div>
  );
}
