import { MessageSquare, History, Sprout, Settings, type LucideIcon } from "lucide-react";

import type { MessageKey } from "@/lib/i18n";

export interface NavItem {
  href: string;
  icon: LucideIcon;
  labelKey: MessageKey;
}

/** Primary navigation (PRD §5.2). Chat is home. */
export const NAV_ITEMS: NavItem[] = [
  { href: "/", icon: MessageSquare, labelKey: "nav.chat" },
  { href: "/history", icon: History, labelKey: "nav.history" },
  { href: "/farm", icon: Sprout, labelKey: "nav.farm" },
  { href: "/settings", icon: Settings, labelKey: "nav.settings" },
];
