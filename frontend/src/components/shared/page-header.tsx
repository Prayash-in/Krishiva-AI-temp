"use client";

import { ArrowLeft } from "lucide-react";
import { useRouter } from "next/navigation";
import type { ReactNode } from "react";

import { IconButton } from "@/components/ui";

/**
 * Page heading with a back button — secondary pages (Settings, My Farm,
 * History) always offer a way back to chat.
 */
export function PageHeader({
  title,
  subtitle,
}: {
  title: string;
  subtitle?: ReactNode;
}) {
  const router = useRouter();

  return (
    <header className="mb-6">
      <div className="flex items-center gap-2">
        <IconButton
          label="Go back"
          size="sm"
          className="-ml-2"
          onClick={() => {
            if (window.history.length > 1) router.back();
            else router.push("/");
          }}
        >
          <ArrowLeft className="size-5" aria-hidden />
        </IconButton>
        <h1 className="text-2xl font-semibold tracking-tight text-text-primary">
          {title}
        </h1>
      </div>
      {subtitle ? (
        <p className="mt-1 pl-9 text-sm text-text-secondary">{subtitle}</p>
      ) : null}
    </header>
  );
}
