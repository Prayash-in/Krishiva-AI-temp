import { forwardRef, type ButtonHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
export type ButtonSize = "sm" | "md" | "lg";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

const VARIANTS: Record<ButtonVariant, string> = {
  primary:
    "bg-accent text-text-inverse hover:enabled:bg-accent-hover shadow-sm",
  secondary:
    "bg-surface-elevated text-text-primary border border-border hover:enabled:bg-surface-hover",
  ghost: "text-text-secondary hover:enabled:bg-surface-hover",
  danger:
    "bg-error-subtle text-error hover:enabled:bg-error hover:enabled:text-text-inverse",
};

const SIZES: Record<ButtonSize, string> = {
  sm: "h-9 px-3 text-sm gap-1.5 rounded-md",
  md: "h-11 px-4 text-base gap-2 rounded-md",
  lg: "h-12 px-5 text-base gap-2 rounded-lg",
};

/** The single button primitive (PRD RULE 100/102/106). */
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", type, ...props }, ref) => (
    <button
      ref={ref}
      type={type ?? "button"}
      className={cn(
        "inline-flex select-none items-center justify-center font-medium transition-colors",
        "duration-[var(--duration-fast)] disabled:cursor-not-allowed disabled:opacity-50",
        VARIANTS[variant],
        SIZES[size],
        className,
      )}
      {...props}
    />
  ),
);
Button.displayName = "Button";
