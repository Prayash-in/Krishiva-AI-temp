/**
 * Domain types.
 *
 * The API-facing shapes (`QueryRequest`, `QueryResponse`, `Diagnosis`,
 * `Source`, `ApiError`) mirror the backend wire contract exactly
 * (`backend/schemas/query.py`, `backend/schemas/errors.py`). The rest are
 * client-only shapes for conversations, which the MVP backend does not persist.
 */

/** Languages the engine actually supports (`engine/knowledge_base/enums.py`). */
export type LanguageCode = "en" | "hi" | "bn" | "as";

export interface QueryRequest {
  query: string;
  language?: LanguageCode | null;
  region?: string | null;
  crop?: string | null;
}

export interface Diagnosis {
  problem: string;
  /** 0.0–1.0 as returned by the engine. */
  confidence: number;
}

export interface Source {
  id: string;
  title: string;
  score?: number | null;
}

export interface QueryResponse {
  query: string;
  language: LanguageCode;
  answer: string;
  diagnosis?: Diagnosis | null;
  sources: Source[];
  request_id: string;
}

/** The backend error envelope: `{ error: { code, message, request_id } }`. */
export interface ApiErrorBody {
  error: {
    code: string;
    message: string;
    request_id: string;
  };
}

export type ConfidenceTier = "high" | "medium" | "low";

export type FeedbackVote = "up" | "down" | null;

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  /** Raw text (user query, or assistant markdown answer). */
  content: string;
  /** Present on assistant messages that carry a diagnosis. */
  diagnosis?: Diagnosis | null;
  sources?: Source[];
  language?: LanguageCode;
  createdAt: number;
  /** Assistant-only UI state. */
  status?: "thinking" | "done" | "error";
  errorMessage?: string;
  feedback?: FeedbackVote;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: number;
  updatedAt: number;
}
