"use client";

import { Menu, PanelLeft } from "lucide-react";
import Link from "next/link";

import { KrishivaLogo } from "@/components/icons/krishiva-logo";
import { ThemeToggle } from "@/components/shared/theme-toggle";
import { IconButton } from "@/components/ui";
import { translatorFor } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";
import { useUiStore } from "@/stores/ui-store";

/** Slim top bar: menu toggle, brand (mobile), theme toggle (PRD P1 layout). */
export function Topbar() {
  const toggleSidebar = useUiStore((s) => s.toggleSidebar);
  const toggleMobileSidebar = useUiStore((s) => s.toggleMobileSidebar);
  const requestNewChat = useUiStore((s) => s.requestNewChat);
  const language = useFarmStore((s) => s.language);
  const t = translatorFor(language);

  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-divider bg-transparent px-3">
      <div className="flex items-center gap-1">
        {/* Mobile: open the slide-in drawer */}
        <IconButton
          label="Open menu"
          onClick={toggleMobileSidebar}
          className="lg:hidden"
        >
          <Menu className="size-5" aria-hidden />
        </IconButton>
        {/* Desktop: collapse/expand the sidebar */}
        <IconButton
          label="Toggle sidebar"
          onClick={toggleSidebar}
          className="hidden lg:inline-flex"
        >
          <PanelLeft className="size-5" aria-hidden />
        </IconButton>
        <Link
          href="/"
          onClick={requestNewChat}
          className="flex items-center gap-2 lg:hidden"
        >
          <KrishivaLogo className="size-6" />
          <span className="text-base font-semibold tracking-tight text-text-primary">
            {t("app.name")}
          </span>
        </Link>
      </div>

      <div className="flex items-center gap-1">
        <ThemeToggle />
      </div>
    </header>
  );
}
