"use client";

import { History, MessageSquare, Trash2 } from "lucide-react";
import Link from "next/link";

import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { Button, IconButton } from "@/components/ui";
import { useMounted } from "@/hooks/use-mounted";
import { translate } from "@/lib/i18n";
import { relativeDay } from "@/lib/utils";
import { useChatStore } from "@/stores/chat-store";
import { useFarmStore } from "@/stores/farm-store";
import type { Conversation } from "@/types";

function groupByDay(conversations: Conversation[]) {
  const groups = new Map<string, Conversation[]>();
  for (const c of [...conversations].sort((a, b) => b.updatedAt - a.updatedAt)) {
    const key = relativeDay(c.updatedAt);
    const list = groups.get(key) ?? [];
    list.push(c);
    groups.set(key, list);
  }
  return [...groups.entries()];
}

/** Chronological list of past conversations (PRD P3). */
export default function HistoryPage() {
  const mounted = useMounted();
  const language = useFarmStore((s) => s.language);
  const conversations = useChatStore((s) => s.conversations);
  const deleteConversation = useChatStore((s) => s.deleteConversation);

  if (!mounted) return null;

  if (conversations.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <EmptyState
          icon={History}
          title={translate(language, "history.empty.title")}
          subtext={translate(language, "history.empty.subtext")}
          action={
            <Link href="/">
              <Button>{translate(language, "history.empty.cta")}</Button>
            </Link>
          }
        />
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-3xl px-4 py-6">
        <PageHeader title={translate(language, "history.title")} />

        <div className="flex flex-col gap-6">
          {groupByDay(conversations).map(([day, list]) => (
            <section key={day}>
              <h2 className="mb-2 text-xs font-medium uppercase tracking-wide text-text-tertiary">
                {day}
              </h2>
              <ul className="flex flex-col gap-1">
                {list.map((c) => (
                  <li key={c.id} className="group relative">
                    <Link
                      href={`/c/${c.id}`}
                      className="flex items-center gap-3 rounded-lg border border-border bg-surface-elevated px-4 py-3 pr-12 shadow-sm transition-colors duration-[var(--duration-fast)] hover:bg-surface-hover"
                    >
                      <MessageSquare
                        className="size-4 shrink-0 text-text-tertiary"
                        aria-hidden
                      />
                      <span className="truncate text-sm text-text-primary">
                        {c.title}
                      </span>
                    </Link>
                    <IconButton
                      label={`Delete: ${c.title}`}
                      size="sm"
                      onClick={() => deleteConversation(c.id)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 focus-visible:opacity-100 group-hover:opacity-100"
                    >
                      <Trash2 className="size-4" aria-hidden />
                    </IconButton>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}
