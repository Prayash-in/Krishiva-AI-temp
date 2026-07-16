import { create } from "zustand";
import { persist } from "zustand/middleware";

import { LOCALSTORAGE_KEYS } from "@/lib/constants";

export type ThemePreference = "light" | "dark" | "system";

interface UiState {
  theme: ThemePreference;
  /** Desktop sidebar collapsed/expanded (persisted). */
  sidebarOpen: boolean;
  /** Mobile slide-in drawer visibility (never persisted). */
  mobileSidebarOpen: boolean;
  /**
   * Bumped by "New chat". The home ChatView keeps its thread id in local
   * state after a replaceState URL swap, so a Link to "/" alone can't reset
   * it — this nonce tells it to start fresh.
   */
  chatResetNonce: number;
  requestNewChat: () => void;
  setTheme: (theme: ThemePreference) => void;
  toggleSidebar: () => void;
  toggleMobileSidebar: () => void;
  setMobileSidebarOpen: (open: boolean) => void;
}

/** UI-only state: theme preference and sidebar visibility (PRD §16.2 providers). */
export const useUiStore = create<UiState>()(
  persist(
    (set) => ({
      theme: "system",
      sidebarOpen: true,
      mobileSidebarOpen: false,
      chatResetNonce: 0,
      requestNewChat: () =>
        set((state) => ({ chatResetNonce: state.chatResetNonce + 1 })),
      setTheme: (theme) => set({ theme }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      toggleMobileSidebar: () =>
        set((state) => ({ mobileSidebarOpen: !state.mobileSidebarOpen })),
      setMobileSidebarOpen: (mobileSidebarOpen) => set({ mobileSidebarOpen }),
    }),
    {
      name: LOCALSTORAGE_KEYS.ui,
      partialize: (state) => ({
        theme: state.theme,
        sidebarOpen: state.sidebarOpen,
      }),
    },
  ),
);
