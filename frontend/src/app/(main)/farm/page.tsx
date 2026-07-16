"use client";

import { Check, MapPin, Sprout } from "lucide-react";
import { useState } from "react";

import { CropSelector } from "@/components/farm/crop-selector";
import { LanguagePicker } from "@/components/shared/language-picker";
import { PageHeader } from "@/components/shared/page-header";
import { Button } from "@/components/ui";
import { useMounted } from "@/hooks/use-mounted";
import { translate } from "@/lib/i18n";
import { useFarmStore } from "@/stores/farm-store";

/**
 * My Farm (PRD P6). Lightweight profile used as query context. Card-based,
 * persisted locally. The "location" is free text sent to the engine as
 * `region` — the MVP has no map/geocoding backend.
 */
export default function FarmPage() {
  const mounted = useMounted();
  const region = useFarmStore((s) => s.region);
  const setRegion = useFarmStore((s) => s.setRegion);
  const crops = useFarmStore((s) => s.crops);
  const toggleCrop = useFarmStore((s) => s.toggleCrop);
  const language = useFarmStore((s) => s.language);
  const setLanguage = useFarmStore((s) => s.setLanguage);
  const setOnboarded = useFarmStore((s) => s.setOnboarded);

  const [regionDraft, setRegionDraft] = useState(region);
  const [saved, setSaved] = useState(false);

  if (!mounted) return null;

  const onSave = () => {
    setRegion(regionDraft.trim());
    setOnboarded(true);
    setSaved(true);
    window.setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-2xl px-4 py-6">
        <PageHeader
          title={translate(language, "farm.title")}
          subtitle={translate(language, "farm.subtitle")}
        />

        <div className="flex flex-col gap-4">
          {/* Location */}
          <section className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
            <label
              htmlFor="farm-location"
              className="flex items-center gap-2 text-sm font-medium text-text-primary"
            >
              <MapPin className="size-4 text-accent" aria-hidden />
              {translate(language, "farm.location")}
            </label>
            <input
              id="farm-location"
              type="text"
              value={regionDraft}
              onChange={(e) => setRegionDraft(e.target.value)}
              placeholder={translate(language, "farm.locationPlaceholder")}
              className="mt-3 h-11 w-full rounded-md border border-border bg-surface-inset px-3 text-base text-text-primary placeholder:text-text-tertiary focus:border-border-strong focus:outline-none"
            />
          </section>

          {/* Crops */}
          <section className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
            <h2 className="flex items-center gap-2 text-sm font-medium text-text-primary">
              <Sprout className="size-4 text-accent" aria-hidden />
              {translate(language, "farm.crops")}
            </h2>
            <div className="mt-3">
              <CropSelector selected={crops} onToggle={toggleCrop} />
            </div>
          </section>

          {/* Language */}
          <section className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
            <h2 className="text-sm font-medium text-text-primary">
              {translate(language, "farm.language")}
            </h2>
            <div className="mt-3">
              <LanguagePicker value={language} onChange={setLanguage} />
            </div>
          </section>

          <div className="flex items-center gap-3">
            <Button onClick={onSave}>{translate(language, "farm.save")}</Button>
            {saved ? (
              <span
                role="status"
                className="inline-flex items-center gap-1 text-sm text-success"
              >
                <Check className="size-4" aria-hidden />
                {translate(language, "farm.saved")}
              </span>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
