"use client";

import { useMutation } from "@tanstack/react-query";
import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError, postQuery } from "@/lib/api";
import { translate } from "@/lib/i18n";
import { makeId } from "@/lib/utils";
import { useChatStore } from "@/stores/chat-store";
import { useFarmStore } from "@/stores/farm-store";
import { useUiStore } from "@/stores/ui-store";
import type { ChatMessage, FeedbackVote, QueryResponse } from "@/types";

interface DispatchVars {
  conversationId: string;
  assistantId: string;
  query: string;
}

function assistantPlaceholder(): ChatMessage {
  return {
    id: makeId(),
    role: "assistant",
    content: "",
    status: "thinking",
    createdAt: Date.now(),
  };
}

/**
 * Owns a single conversation's send/stop/retry lifecycle. Each turn is one
 * `POST /api/v1/query` (the MVP engine is non-streaming), driven through a
 * TanStack Query mutation (PRD RULE 110). The farm profile supplies
 * `region`/`crop` context on every request.
 */
export function useChat(initialConversationId?: string) {
  const [activeId, setActiveId] = useState<string | null>(
    initialConversationId ?? null,
  );
  const abortRef = useRef<AbortController | null>(null);
  // Assistant message ids whose request is in flight from THIS hook instance.
  // The stale-"thinking" cleanup below must never flip these to errors — they
  // are live, not orphaned.
  const inFlightIds = useRef<Set<string>>(new Set());

  const language = useFarmStore((s) => s.language);
  const region = useFarmStore((s) => s.region);
  const crops = useFarmStore((s) => s.crops);

  const conversations = useChatStore((s) => s.conversations);
  const createConversation = useChatStore((s) => s.createConversation);
  const appendMessage = useChatStore((s) => s.appendMessage);
  const updateMessage = useChatStore((s) => s.updateMessage);
  const setFeedbackStore = useChatStore((s) => s.setFeedback);
  const deleteConversation = useChatStore((s) => s.deleteConversation);

  const conversation = conversations.find((c) => c.id === activeId);

  // "New chat" pressed. The home ChatView swaps the URL via replaceState
  // after the first send, so router navigation to "/" is a no-op there —
  // this nonce is the explicit reset signal.
  const chatResetNonce = useUiStore((s) => s.chatResetNonce);
  const [seenResetNonce, setSeenResetNonce] = useState(chatResetNonce);
  if (chatResetNonce !== seenResetNonce) {
    setSeenResetNonce(chatResetNonce);
    if (!initialConversationId) setActiveId(null);
  }
  useEffect(() => {
    if (chatResetNonce === 0 || initialConversationId) return;
    abortRef.current?.abort();
    window.history.replaceState(null, "", "/");
  }, [chatResetNonce, initialConversationId]);

  const hasFarmContext = region.trim().length > 0 || crops.length > 0;

  // Normalize any 'thinking' turns left dangling by a closed/reloaded tab into
  // errors, so history never shows a permanently-spinning message. Skip turns
  // whose request is still in flight in this instance (e.g. the placeholder of
  // a just-sent first message) — those are live, not orphaned.
  useEffect(() => {
    if (!conversation) return;
    for (const m of conversation.messages) {
      if (
        m.role === "assistant" &&
        m.status === "thinking" &&
        !inFlightIds.current.has(m.id)
      ) {
        updateMessage(conversation.id, m.id, {
          status: "error",
          errorMessage: translate(language, "error.generic"),
        });
      }
    }
    // Run once per conversation id.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [conversation?.id]);

  const mutation = useMutation<QueryResponse, unknown, DispatchVars>({
    mutationFn: ({ query }) => {
      const controller = new AbortController();
      abortRef.current = controller;
      return postQuery(
        {
          query,
          language,
          region: region.trim() || null,
          crop: crops[0] ?? null,
        },
        controller.signal,
      );
    },
    onSuccess: (data, vars) => {
      updateMessage(vars.conversationId, vars.assistantId, {
        content: data.answer,
        diagnosis: data.diagnosis ?? null,
        sources: data.sources,
        language: data.language,
        status: "done",
      });
    },
    onError: (error, vars) => {
      if (error instanceof DOMException && error.name === "AbortError") {
        // Stopped by the user — drop the empty placeholder.
        return;
      }
      const message =
        error instanceof ApiError
          ? error.message
          : translate(language, "error.generic");
      updateMessage(vars.conversationId, vars.assistantId, {
        status: "error",
        errorMessage: message,
      });
    },
    onSettled: (_data, _error, vars) => {
      abortRef.current = null;
      inFlightIds.current.delete(vars.assistantId);
    },
  });

  const dispatch = useCallback(
    (conversationId: string, query: string) => {
      const placeholder = assistantPlaceholder();
      appendMessage(conversationId, placeholder);
      inFlightIds.current.add(placeholder.id);
      mutation.mutate({
        conversationId,
        assistantId: placeholder.id,
        query,
      });
    },
    [appendMessage, mutation],
  );

  const send = useCallback(
    (text: string) => {
      const userMessage: ChatMessage = {
        id: makeId(),
        role: "user",
        content: text,
        createdAt: Date.now(),
      };

      if (activeId) {
        appendMessage(activeId, userMessage);
        dispatch(activeId, text);
        return;
      }

      const created = createConversation(userMessage);
      setActiveId(created.id);
      // Reflect the new thread in the URL without a remount that would
      // interrupt the in-flight request.
      window.history.replaceState(null, "", `/c/${created.id}`);
      dispatch(created.id, text);
    },
    [activeId, appendMessage, createConversation, dispatch],
  );

  const stop = useCallback(() => {
    abortRef.current?.abort();
    // Remove the pending placeholder (nothing streamed to keep).
    if (conversation) {
      const last = conversation.messages[conversation.messages.length - 1];
      if (last?.role === "assistant" && last.status === "thinking") {
        // Trim by rewriting messages without the placeholder.
        useChatStore.setState((state) => ({
          conversations: state.conversations.map((c) =>
            c.id === conversation.id
              ? { ...c, messages: c.messages.filter((m) => m.id !== last.id) }
              : c,
          ),
        }));
      }
    }
  }, [conversation]);

  const retry = useCallback(
    (assistantId: string) => {
      if (!conversation) return;
      const index = conversation.messages.findIndex((m) => m.id === assistantId);
      if (index <= 0) return;
      const userMessage = conversation.messages[index - 1];
      if (userMessage.role !== "user") return;
      updateMessage(conversation.id, assistantId, {
        status: "thinking",
        errorMessage: undefined,
      });
      inFlightIds.current.add(assistantId);
      mutation.mutate({
        conversationId: conversation.id,
        assistantId,
        query: userMessage.content,
      });
    },
    [conversation, mutation, updateMessage],
  );

  const setFeedback = useCallback(
    (messageId: string, vote: FeedbackVote) => {
      if (conversation) setFeedbackStore(conversation.id, messageId, vote);
    },
    [conversation, setFeedbackStore],
  );

  return {
    conversation,
    messages: conversation?.messages ?? [],
    isBusy: mutation.isPending,
    hasFarmContext,
    send,
    stop,
    retry,
    setFeedback,
    deleteConversation,
  };
}
