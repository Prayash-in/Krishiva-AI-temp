"use client";

import { useEffect, useState } from "react";

/**
 * True after the first client render. Used to gate rendering of state that
 * comes from localStorage (Zustand persist) so server and client markup match
 * on the first paint and avoid hydration mismatches.
 */
export function useMounted(): boolean {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  return mounted;
}
