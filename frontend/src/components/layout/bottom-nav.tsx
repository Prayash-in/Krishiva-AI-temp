"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { NAV_ITEMS } from "@/components/layout/nav-config";
import { translatorFor } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { useFarmStore } from "@/stores/farm-store";

/** Mobile bottom navigation (PRD §5.3). Hidden on desktop. */
export function BottomNav() {
  const pathname = usePathname();
  const language = useFarmStore((s) => s.language);
  const t = translatorFor(language);

  const isActive = (href: string) =>
    href === "/"
      ? pathname === "/" || pathname.startsWith("/c/")
      : pathname === href;

  return (
    <nav
      aria-label="Primary"
      className="flex shrink-0 items-stretch border-t border-border bg-bg lg:hidden"
    >
      {NAV_ITEMS.map((item) => {
        const active = isActive(item.href);
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            aria-current={active ? "page" : undefined}
            className={cn(
              "flex flex-1 flex-col items-center gap-1 py-2 text-xs font-medium",
              "transition-colors duration-[var(--duration-fast)]",
              active ? "text-accent" : "text-text-tertiary",
            )}
          >
            <Icon className="size-5" aria-hidden />
            {t(item.labelKey)}
          </Link>
        );
      })}
    </nav>
  );
}
