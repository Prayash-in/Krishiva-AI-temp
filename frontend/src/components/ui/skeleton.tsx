import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

/** Shimmer placeholder for loading states (PRD §11.4). */
export function Skeleton({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      aria-hidden
      className={cn(
        "relative overflow-hidden rounded-md bg-skeleton-base",
        "motion-safe:after:absolute motion-safe:after:inset-0 motion-safe:after:content-['']",
        "motion-safe:after:-translate-x-full motion-safe:after:animate-[shimmer_1.6s_infinite]",
        "motion-safe:after:bg-gradient-to-r motion-safe:after:from-transparent",
        "motion-safe:after:via-skeleton-shine motion-safe:after:to-transparent",
        className,
      )}
      {...props}
    />
  );
}
