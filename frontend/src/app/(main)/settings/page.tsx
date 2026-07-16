"use client";

import { Monitor, Moon, Sun } from "lucide-react";

import { LanguagePicker } from "@/components/shared/language-picker";
import { PageHeader } from "@/components/shared/page-header";
import { useMounted } from "@/hooks/use-mounted";
import { translate } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";
import { useUiStore, type ThemePreference } from "@/stores/ui-store";

const THEME_OPTIONS: {
  value: ThemePreference;
  icon: typeof Sun;
  labelKey: "settings.theme.light" | "settings.theme.dark" | "settings.theme.system";
}[] = [
  { value: "light", icon: Sun, labelKey: "settings.theme.light" },
  { value: "dark", icon: Moon, labelKey: "settings.theme.dark" },
  { value: "system", icon: Monitor, labelKey: "settings.theme.system" },
];

/** Settings (PRD P7): appearance + language. */
export default function SettingsPage() {
  const mounted = useMounted();
  const theme = useUiStore((s) => s.theme);
  const setTheme = useUiStore((s) => s.setTheme);
  const language = useFarmStore((s) => s.language);
  const setLanguage = useFarmStore((s) => s.setLanguage);

  if (!mounted) return null;

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-2xl px-4 py-6">
        <PageHeader title={translate(language, "settings.title")} />

        <div className="flex flex-col gap-4">
          {/* Appearance */}
          <section className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
            <h2 className="text-sm font-medium text-text-primary">
              {translate(language, "settings.appearance")}
            </h2>
            <p className="mb-3 mt-1 text-xs text-text-secondary">
              {translate(language, "settings.theme")}
            </p>
            <div
              className="flex gap-2"
              role="radiogroup"
              aria-label={translate(language, "settings.theme")}
            >
              {THEME_OPTIONS.map((option) => {
                const Icon = option.icon;
                const active = theme === option.value;
                return (
                  <button
                    key={option.value}
                    type="button"
                    role="radio"
                    aria-checked={active}
                    onClick={() => setTheme(option.value)}
                    className={cn(
                      "flex flex-1 flex-col items-center gap-2 rounded-lg border px-3 py-4 text-sm font-medium",
                      "transition-colors duration-[var(--duration-fast)]",
                      active
                        ? "border-accent bg-accent-subtle text-accent"
                        : "border-border text-text-secondary hover:bg-surface-hover",
                    )}
                  >
                    <Icon className="size-5" aria-hidden />
                    {translate(language, option.labelKey)}
                  </button>
                );
              })}
            </div>
          </section>

          {/* Language */}
          <section className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
            <h2 className="mb-3 text-sm font-medium text-text-primary">
              {translate(language, "settings.language")}
            </h2>
            <LanguagePicker
              value={language}
              onChange={setLanguage}
              variant="list"
            />
          </section>
        </div>
      </div>
    </div>
  );
}
