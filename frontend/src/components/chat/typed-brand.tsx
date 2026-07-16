"use client";

import { useEffect, useState, useSyncExternalStore } from "react";

/** Brand name in each supported language, cycled by the typing loop. */
const BRAND_WORDS = ["Krishiva", "कृषिवा", "কৃষিভা", "কৃষিৱা"];

const TYPE_MS = 90;
const ERASE_MS = 45;
const HOLD_MS = 2000;

const MOTION_QUERY = "(prefers-reduced-motion: reduce)";

function subscribeToMotionPreference(callback: () => void) {
  const query = window.matchMedia(MOTION_QUERY);
  query.addEventListener("change", callback);
  return () => query.removeEventListener("change", callback);
}

/**
 * The hero brand heading: types "Krishiva", holds for 2s, erases and retypes
 * it in the next language, looping forever. Falls back to the static English
 * word for users who prefer reduced motion.
 */
export function TypedBrand({ className }: { className?: string }) {
  const [wordIndex, setWordIndex] = useState(0);
  const [charCount, setCharCount] = useState(0);
  const [erasing, setErasing] = useState(false);
  const reducedMotion = useSyncExternalStore(
    subscribeToMotionPreference,
    () => window.matchMedia(MOTION_QUERY).matches,
    () => true, // SSR: render the static word until the client takes over
  );

  // Split on code points so Devanagari/Bangla clusters don't break mid-glyph.
  const chars = Array.from(BRAND_WORDS[wordIndex]);

  useEffect(() => {
    if (reducedMotion) return;

    let delay: number;
    let next: () => void;

    if (!erasing && charCount < chars.length) {
      delay = TYPE_MS;
      next = () => setCharCount((n) => n + 1);
    } else if (!erasing) {
      delay = HOLD_MS;
      next = () => setErasing(true);
    } else if (charCount > 0) {
      delay = ERASE_MS;
      next = () => setCharCount((n) => n - 1);
    } else {
      delay = 300;
      next = () => {
        setErasing(false);
        setWordIndex((i) => (i + 1) % BRAND_WORDS.length);
      };
    }

    const timer = window.setTimeout(next, delay);
    return () => window.clearTimeout(timer);
  }, [charCount, erasing, chars.length, reducedMotion]);

  return (
    <h1 className={className} aria-label="Krishiva">
      <span aria-hidden>
        {reducedMotion ? BRAND_WORDS[0] : chars.slice(0, charCount).join("")}
      </span>
      {!reducedMotion ? (
        <span
          aria-hidden
          className="ml-2 inline-block w-[4px] self-center rounded-full bg-accent motion-safe:animate-[caret-blink_1.1s_steps(1)_infinite]"
          style={{ height: "1.15em" }}
        />
      ) : null}
    </h1>
  );
}
