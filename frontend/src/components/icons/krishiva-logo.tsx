import { cn } from "@/lib/utils";

/**
 * The Krishiva mark: a single sprouting leaf. Uses `currentColor` so it
 * inherits the accent from its container. Decorative by default (PRD RULE 107).
 */
export function KrishivaLogo({
  className,
  title,
}: {
  className?: string;
  title?: string;
}) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      role={title ? "img" : "presentation"}
      aria-label={title}
      aria-hidden={title ? undefined : true}
      className={cn("text-accent", className)}
    >
      {title ? <title>{title}</title> : null}
      {/* Stem */}
      <path d="M12 21c0-4.5 0-7 0-9.5" stroke="currentColor" />
      {/* Right leaf */}
      <path
        d="M12 12c0-4 2.5-6.5 7-7-.5 4.5-3 7-7 7Z"
        stroke="currentColor"
        className="fill-accent/15"
      />
      {/* Left leaf */}
      <path
        d="M12 15c0-3.2-2-5.2-5.5-5.6C6.9 12.6 8.8 15 12 15Z"
        stroke="currentColor"
        className="fill-accent/10"
      />
    </svg>
  );
}
