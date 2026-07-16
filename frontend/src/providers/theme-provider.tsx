"use client";

import { useEffect, type ReactNode } from "react";

import { useUiStore } from "@/stores/ui-store";

/**
 * Applies the theme preference by toggling the `dark` class on <html>
 * (PRD RULE 206). Tracks the OS preference when set to "system".
 */
export function ThemeProvider({ children }: { children: ReactNode }) {
  const theme = useUiStore((s) => s.theme);

  useEffect(() => {
    const root = document.documentElement;
    const media = window.matchMedia("(prefers-color-scheme: dark)");

    const apply = () => {
      const isDark = theme === "dark" || (theme === "system" && media.matches);
      root.classList.toggle("dark", isDark);
    };

    apply();
    if (theme === "system") {
      media.addEventListener("change", apply);
      return () => media.removeEventListener("change", apply);
    }
  }, [theme]);

  return <>{children}</>;
}
