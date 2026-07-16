import { Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";

/** Indeterminate loading spinner. */
export function Spinner({
  className,
  label = "Loading",
}: {
  className?: string;
  label?: string;
}) {
  return (
    <Loader2
      role="status"
      aria-label={label}
      className={cn("size-5 animate-spin text-text-tertiary", className)}
    />
  );
}
