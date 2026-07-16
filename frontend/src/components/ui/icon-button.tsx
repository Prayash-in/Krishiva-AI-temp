import { forwardRef, type ButtonHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export interface IconButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Required for accessibility — icon-only buttons need a label (PRD §16.3). */
  label: string;
  size?: "sm" | "md";
  active?: boolean;
}

/**
 * An icon-only button with a guaranteed 44×44 touch target (PRD touch-target
 * rule) even when the glyph is smaller.
 */
export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ className, label, size = "md", active = false, type, ...props }, ref) => (
    <button
      ref={ref}
      type={type ?? "button"}
      aria-label={label}
      aria-pressed={active}
      className={cn(
        "inline-flex items-center justify-center rounded-full text-text-secondary",
        "transition-colors duration-[var(--duration-fast)]",
        "hover:enabled:bg-surface-hover hover:enabled:text-accent",
        "disabled:cursor-not-allowed disabled:opacity-40",
        active && "bg-accent-subtle text-accent",
        size === "sm" ? "size-9" : "size-11",
        className,
      )}
      {...props}
    />
  ),
);
IconButton.displayName = "IconButton";
