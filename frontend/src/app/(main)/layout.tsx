import type { ReactNode } from "react";

import { AppShell } from "@/components/layout/app-shell";

/** Shared frame for all authenticated app pages (PRD §16.5 `(main)` group). */
export default function MainLayout({ children }: { children: ReactNode }) {
  return <AppShell>{children}</AppShell>;
}
