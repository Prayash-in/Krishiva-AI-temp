import type { LanguageCode } from "@/types";

/**
 * Lightweight UI string catalog.
 *
 * The PRD calls for next-intl; for the MVP we centralize strings in a typed
 * dictionary so no user-facing copy is hardcoded in components (PRD RULE 108),
 * while keeping the bundle small. English and Hindi are provided; other
 * languages fall back to English until translated.
 */
const en = {
  "app.name": "Krishiva AI",
  "app.tagline": "Your farming assistant",
  "nav.chat": "Chat",
  "nav.history": "History",
  "nav.farm": "My Farm",
  "nav.settings": "Settings",
  "chat.newChat": "New chat",
  "chat.greeting": "Namaste, I'm",
  "chat.subgreeting":
    "Ask me about your crops, upload a photo for diagnosis, or try one of these:",
  "chat.placeholder": "Ask anything about your crop…",
  "chat.send": "Send",
  "chat.stop": "Stop",
  "chat.thinking": "Krishiva is thinking…",
  "chat.stillWorking": "Still working on this…",
  "chat.newContent": "New content",
  "chat.retry": "Try again",
  "chat.sources": "Sources",
  "chat.generalGuidance":
    "This is general guidance. For specific advice, consult a local agricultural officer.",
  "chat.contextBadge": "Using your farm profile",
  "confidence.high": "High confidence",
  "confidence.medium": "Moderate confidence",
  "confidence.low": "Low confidence — consider consulting an expert",
  "confidence.lowCallout":
    "This diagnosis has low confidence. Please verify with a local expert or upload a clearer photo.",
  "diagnosis.title": "Diagnosis",
  "feedback.up": "Helpful",
  "feedback.down": "Not helpful",
  "feedback.thanks": "Thanks for your feedback",
  "history.title": "History",
  "history.empty.title": "No conversations yet",
  "history.empty.subtext":
    "Your farming questions and diagnoses will appear here. Start your first conversation!",
  "history.empty.cta": "Start a conversation",
  "history.delete": "Delete",
  "farm.title": "My Farm",
  "farm.subtitle": "Krishiva uses this to tailor every answer.",
  "farm.location": "Location",
  "farm.locationPlaceholder": "e.g. Nashik, Maharashtra",
  "farm.crops": "Crops",
  "farm.language": "Preferred language",
  "farm.save": "Save",
  "farm.saved": "Saved",
  "settings.title": "Settings",
  "settings.appearance": "Appearance",
  "settings.theme": "Theme",
  "settings.theme.light": "Light",
  "settings.theme.dark": "Dark",
  "settings.theme.system": "System",
  "settings.language": "Language",
  "common.offline": "You're offline. Your messages will send when you reconnect.",
  "common.backOnline": "You're back online.",
  "error.generic":
    "Krishiva couldn't process your question right now. Let's try again.",
} as const;

export type MessageKey = keyof typeof en;

const hi: Partial<Record<MessageKey, string>> = {
  "app.tagline": "आपका खेती सहायक",
  "nav.chat": "चैट",
  "nav.history": "इतिहास",
  "nav.farm": "मेरा खेत",
  "nav.settings": "सेटिंग्स",
  "chat.newChat": "नई चैट",
  "chat.greeting": "नमस्ते, मैं हूँ",
  "chat.subgreeting":
    "अपनी फसल के बारे में पूछें, या इनमें से कोई एक आज़माएँ:",
  "chat.placeholder": "अपनी फसल के बारे में कुछ भी पूछें…",
  "chat.thinking": "कृषिवा सोच रहा है…",
  "chat.sources": "स्रोत",
  "diagnosis.title": "निदान",
  "confidence.high": "उच्च विश्वास",
  "confidence.medium": "मध्यम विश्वास",
  "confidence.low": "कम विश्वास — किसी विशेषज्ञ से सलाह लें",
};

const catalogs: Record<LanguageCode, Partial<Record<MessageKey, string>>> = {
  en,
  hi,
  bn: {},
  as: {},
};

/** Resolve a message key for a language, falling back to English. */
export function translate(lang: LanguageCode, key: MessageKey): string {
  return catalogs[lang]?.[key] ?? en[key];
}

/** Curried translator for a fixed language. */
export function translatorFor(lang: LanguageCode) {
  return (key: MessageKey): string => translate(lang, key);
}
