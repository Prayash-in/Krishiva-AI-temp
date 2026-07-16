import { create } from "zustand";
import { persist } from "zustand/middleware";

import { DEFAULT_LANGUAGE, LOCALSTORAGE_KEYS } from "@/lib/constants";
import type { LanguageCode } from "@/types";

interface FarmState {
  /** Free-text location, sent to the engine as `region`. */
  region: string;
  crops: string[];
  language: LanguageCode;
  /** True once the user has completed (or skipped) onboarding. */
  onboarded: boolean;
  setRegion: (region: string) => void;
  setCrops: (crops: string[]) => void;
  toggleCrop: (crop: string) => void;
  setLanguage: (language: LanguageCode) => void;
  setOnboarded: (onboarded: boolean) => void;
}

/**
 * The lightweight farm profile (PRD F9). Persisted locally and used as
 * context (`region`, `crop`) on every query. The MVP backend does not store
 * this server-side.
 */
export const useFarmStore = create<FarmState>()(
  persist(
    (set) => ({
      region: "",
      crops: [],
      language: DEFAULT_LANGUAGE,
      onboarded: false,
      setRegion: (region) => set({ region }),
      setCrops: (crops) => set({ crops }),
      toggleCrop: (crop) =>
        set((state) => ({
          crops: state.crops.includes(crop)
            ? state.crops.filter((c) => c !== crop)
            : [...state.crops, crop],
        })),
      setLanguage: (language) => set({ language }),
      setOnboarded: (onboarded) => set({ onboarded }),
    }),
    { name: LOCALSTORAGE_KEYS.farm },
  ),
);
