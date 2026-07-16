import type { LanguageCode } from "@/types";

/**
 * Base URL of the Krishiva backend. Overridable via
 * `NEXT_PUBLIC_API_BASE_URL`; defaults to the local uvicorn dev server.
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export const API_PREFIX = "/api/v1";

/** Max query length accepted by the backend (`backend/schemas/query.py`). */
export const MAX_QUERY_LENGTH = 1000;

export interface LanguageOption {
  code: LanguageCode;
  /** Endonym — the language's own name. */
  label: string;
  /** English name, for the settings list. */
  englishLabel: string;
}

/**
 * The four languages the engine currently supports. The PRD lists seven;
 * we surface only what the backend can answer in so the UI never promises
 * a language the engine cannot serve.
 */
export const LANGUAGES: LanguageOption[] = [
  { code: "en", label: "English", englishLabel: "English" },
  { code: "hi", label: "हिन्दी", englishLabel: "Hindi" },
  { code: "bn", label: "বাংলা", englishLabel: "Bengali" },
  { code: "as", label: "অসমীয়া", englishLabel: "Assamese" },
];

export const DEFAULT_LANGUAGE: LanguageCode = "en";

/** Empty-state prompt suggestions (PRD F4). */
export const PROMPT_SUGGESTIONS: string[] = [
  "What's wrong with my tomato leaves?",
  "Best fertilizer for wheat this season",
  "Yellow spots on my paddy leaf",
  "How do I control aphids on my crop?",
];

/** Common crops for the lightweight farm profile (PRD F9). */
export const COMMON_CROPS: string[] = [
  "Rice",
  "Wheat",
  "Tomato",
  "Onion",
  "Potato",
  "Grapes",
  "Cotton",
  "Sugarcane",
  "Maize",
  "Tea",
];

export const LOCALSTORAGE_KEYS = {
  conversations: "krishiva.conversations",
  farm: "krishiva.farm",
  ui: "krishiva.ui",
} as const;
