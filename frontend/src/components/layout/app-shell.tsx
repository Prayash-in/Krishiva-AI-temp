import type { ReactNode } from "react";

import { BottomNav } from "@/components/layout/bottom-nav";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import { OfflineBanner } from "@/components/shared/offline-banner";

/**
 * The app frame: sidebar + topbar + scrollable main + mobile bottom nav
 * (PRD §16.2 layout). Pages render into `children`.
 */
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-dvh overflow-hidden bg-bg">
      <Sidebar />
      <div className="bg-mesh flex min-w-0 flex-1 flex-col">
        <OfflineBanner />
        <Topbar />
        <main className="min-h-0 flex-1 overflow-hidden">{children}</main>
        <BottomNav />
      </div>
    </div>
  );
}
