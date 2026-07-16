"use client";

import { Plus, Trash2, X } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { KrishivaLogo } from "@/components/icons/krishiva-logo";
import { NAV_ITEMS } from "@/components/layout/nav-config";
import { IconButton } from "@/components/ui";
import { useMounted } from "@/hooks/use-mounted";
import { translatorFor } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { useChatStore } from "@/stores/chat-store";
import { useFarmStore } from "@/stores/farm-store";
import { useUiStore } from "@/stores/ui-store";

/**
 * Collapsible left sidebar (desktop) / slide-in drawer (mobile). Holds the
 * New-chat action, conversation history and primary nav (PRD §5.3).
 *
 * Desktop collapse (`sidebarOpen`) and the mobile drawer (`mobileSidebarOpen`)
 * are independent: navigating closes only the mobile drawer, so the desktop
 * sidebar stays put.
 */
export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const mounted = useMounted();
  const open = useUiStore((s) => s.sidebarOpen);
  const mobileOpen = useUiStore((s) => s.mobileSidebarOpen);
  const setMobileOpen = useUiStore((s) => s.setMobileSidebarOpen);
  const requestNewChat = useUiStore((s) => s.requestNewChat);
  const language = useFarmStore((s) => s.language);
  const conversations = useChatStore((s) => s.conversations);
  const deleteConversation = useChatStore((s) => s.deleteConversation);
  const t = translatorFor(language);

  const activeId = pathname.startsWith("/c/") ? pathname.slice(3) : null;

  const closeDrawer = () => setMobileOpen(false);

  const onNewChat = () => {
    requestNewChat();
    closeDrawer();
  };

  const onDelete = (id: string) => {
    deleteConversation(id);
    if (activeId === id) router.push("/");
  };

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen ? (
        <button
          type="button"
          aria-label="Close menu"
          onClick={closeDrawer}
          className="fixed inset-0 z-30 bg-overlay backdrop-blur-[2px] lg:hidden"
        />
      ) : null}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-border bg-surface",
          "transition-transform duration-[var(--duration-moderate)] ease-[var(--ease-out)]",
          "lg:static lg:z-auto lg:translate-x-0",
          mobileOpen ? "translate-x-0 shadow-xl lg:shadow-none" : "-translate-x-full",
          open ? "lg:flex" : "lg:hidden",
        )}
      >
        <div className="flex h-14 shrink-0 items-center justify-between px-4">
          <Link
            href="/"
            className="flex items-center gap-2.5"
            onClick={onNewChat}
          >
            <KrishivaLogo className="size-7" />
            <span className="text-[17px] font-semibold tracking-tight text-text-primary">
              {t("app.name")}
            </span>
          </Link>
          <IconButton
            label="Close menu"
            size="sm"
            className="lg:hidden"
            onClick={closeDrawer}
          >
            <X className="size-5" aria-hidden />
          </IconButton>
        </div>

        <div className="px-3 pt-1">
          <Link
            href="/"
            onClick={onNewChat}
            className={cn(
              "flex h-11 items-center gap-2 rounded-lg border border-border bg-surface-elevated px-3",
              "text-sm font-medium text-text-primary shadow-xs",
              "transition-all duration-[var(--duration-fast)] hover:border-border-strong hover:shadow-sm",
            )}
          >
            <Plus className="size-4 text-accent" aria-hidden />
            {t("chat.newChat")}
          </Link>
        </div>

        {/* Conversation history */}
        <nav
          aria-label="Conversation history"
          className="mt-5 flex-1 overflow-y-auto px-3"
        >
          {mounted && conversations.length > 0 ? (
            <>
              <p className="mb-1.5 px-3 text-[11px] font-medium uppercase tracking-wider text-text-tertiary">
                {t("history.title")}
              </p>
              <ul className="flex flex-col gap-0.5">
                {conversations.map((c) => {
                  const active = c.id === activeId;
                  return (
                    <li key={c.id} className="group relative">
                      <Link
                        href={`/c/${c.id}`}
                        onClick={closeDrawer}
                        className={cn(
                          "flex items-center rounded-md px-3 py-2 pr-9 text-sm",
                          "transition-colors duration-[var(--duration-fast)]",
                          active
                            ? "bg-accent-subtle font-medium text-accent"
                            : "text-text-secondary hover:bg-surface-hover hover:text-text-primary",
                        )}
                      >
                        <span className="truncate">{c.title}</span>
                      </Link>
                      <IconButton
                        label={`Delete conversation: ${c.title}`}
                        size="sm"
                        onClick={() => onDelete(c.id)}
                        className="absolute right-1 top-1/2 size-8 -translate-y-1/2 opacity-0 focus-visible:opacity-100 group-hover:opacity-100"
                      >
                        <Trash2 className="size-4" aria-hidden />
                      </IconButton>
                    </li>
                  );
                })}
              </ul>
            </>
          ) : (
            <p className="px-3 py-2 text-sm text-text-tertiary">
              {mounted ? t("history.empty.title") : ""}
            </p>
          )}
        </nav>

        {/* Primary nav footer */}
        <div className="border-t border-divider p-3">
          <ul className="flex flex-col gap-0.5">
            {NAV_ITEMS.filter((i) => i.href !== "/" && i.href !== "/history").map(
              (item) => {
                const active = pathname === item.href;
                const Icon = item.icon;
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      onClick={closeDrawer}
                      className={cn(
                        "flex items-center gap-3 rounded-md px-3 py-2 text-sm",
                        "transition-colors duration-[var(--duration-fast)]",
                        active
                          ? "bg-accent-subtle font-medium text-accent"
                          : "text-text-secondary hover:bg-surface-hover hover:text-text-primary",
                      )}
                    >
                      <Icon className="size-5" aria-hidden />
                      {t(item.labelKey)}
                    </Link>
                  </li>
                );
              },
            )}
          </ul>
        </div>
      </aside>
    </>
  );
}
