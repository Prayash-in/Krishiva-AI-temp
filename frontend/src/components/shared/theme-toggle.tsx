"use client";

import { Monitor, Moon, Sun } from "lucide-react";

import { IconButton } from "@/components/ui";
import { useMounted } from "@/hooks/use-mounted";
import { useUiStore, type ThemePreference } from "@/stores/ui-store";

const ORDER: ThemePreference[] = ["light", "dark", "system"];
const ICON = { light: Sun, dark: Moon, system: Monitor } as const;
const LABEL = {
  light: "Theme: light",
  dark: "Theme: dark",
  system: "Theme: system",
} as const;

/** Cycles light → dark → system (PRD F24). */
export function ThemeToggle() {
  const mounted = useMounted();
  const theme = useUiStore((s) => s.theme);
  const setTheme = useUiStore((s) => s.setTheme);

  const current = mounted ? theme : "system";
  const Icon = ICON[current];

  const cycle = () => {
    const next = ORDER[(ORDER.indexOf(current) + 1) % ORDER.length];
    setTheme(next);
  };

  return (
    <IconButton label={LABEL[current]} onClick={cycle}>
      <Icon className="size-5" aria-hidden />
    </IconButton>
  );
}
