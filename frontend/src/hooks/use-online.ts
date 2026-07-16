"use client";

import { useEffect, useState } from "react";

/**
 * Tracks connectivity via `navigator.onLine` + online/offline events
 * (PRD RULE 504). Defaults to online during SSR / first paint.
 */
export function useOnline(): boolean {
  const [online, setOnline] = useState(true);

  useEffect(() => {
    setOnline(navigator.onLine);
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener("online", on);
    window.addEventListener("offline", off);
    return () => {
      window.removeEventListener("online", on);
      window.removeEventListener("offline", off);
    };
  }, []);

  return online;
}
