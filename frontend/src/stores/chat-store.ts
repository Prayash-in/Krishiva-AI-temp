import { create } from "zustand";
import { persist } from "zustand/middleware";

import { LOCALSTORAGE_KEYS } from "@/lib/constants";
import { deriveTitle, makeId } from "@/lib/utils";
import type { ChatMessage, Conversation, FeedbackVote } from "@/types";

interface ChatState {
  conversations: Conversation[];
  createConversation: (firstMessage: ChatMessage) => Conversation;
  appendMessage: (conversationId: string, message: ChatMessage) => void;
  updateMessage: (
    conversationId: string,
    messageId: string,
    patch: Partial<ChatMessage>,
  ) => void;
  setFeedback: (
    conversationId: string,
    messageId: string,
    vote: FeedbackVote,
  ) => void;
  deleteConversation: (conversationId: string) => void;
  getConversation: (conversationId: string) => Conversation | undefined;
}

/**
 * Client-side conversation history (PRD F5). The MVP backend is stateless, so
 * threads live in localStorage; each turn is one `POST /api/v1/query`.
 */
export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      conversations: [],

      createConversation: (firstMessage) => {
        const now = Date.now();
        const conversation: Conversation = {
          id: makeId(),
          title: deriveTitle(firstMessage.content),
          messages: [firstMessage],
          createdAt: now,
          updatedAt: now,
        };
        set((state) => ({
          conversations: [conversation, ...state.conversations],
        }));
        return conversation;
      },

      appendMessage: (conversationId, message) =>
        set((state) => ({
          conversations: state.conversations.map((c) =>
            c.id === conversationId
              ? { ...c, messages: [...c.messages, message], updatedAt: Date.now() }
              : c,
          ),
        })),

      updateMessage: (conversationId, messageId, patch) =>
        set((state) => ({
          conversations: state.conversations.map((c) =>
            c.id === conversationId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === messageId ? { ...m, ...patch } : m,
                  ),
                  updatedAt: Date.now(),
                }
              : c,
          ),
        })),

      setFeedback: (conversationId, messageId, vote) =>
        get().updateMessage(conversationId, messageId, { feedback: vote }),

      deleteConversation: (conversationId) =>
        set((state) => ({
          conversations: state.conversations.filter(
            (c) => c.id !== conversationId,
          ),
        })),

      getConversation: (conversationId) =>
        get().conversations.find((c) => c.id === conversationId),
    }),
    { name: LOCALSTORAGE_KEYS.conversations },
  ),
);
