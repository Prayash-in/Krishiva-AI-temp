# Krishiva AI — Frontend (MVP)

A Next.js 15 (App Router) web client for Krishiva AI, the farmer's conversational
copilot. Built to the design language in `krishiva_ai_prd.md` and wired to the
real FastAPI backend contract (`backend/`).

## Stack

- **Next.js 16 / React 19** (App Router, `src/` dir, route groups)
- **TypeScript** (strict)
- **Tailwind CSS v4** with a CSS-variable design-token system (`src/app/globals.css`)
- **Zustand** for UI / chat / farm state (localStorage-persisted)
- **TanStack Query** for the query mutation (all API calls flow through it)
- **Lucide** icons, **react-markdown** for answer rendering

## Running locally

```bash
# 1. Start the backend (from the repo root)
uv run python main.py        # → http://127.0.0.1:8000

# 2. Start the frontend
cd frontend
npm install
cp .env.example .env.local   # points NEXT_PUBLIC_API_BASE_URL at the backend
npm run dev                  # → http://localhost:3000
```

The frontend talks to `POST /api/v1/query`. The backend currently runs a
`StubQueryEngine` (deterministic Rice Blast response) so the whole flow is
exercisable before the real engine lands.

## What's built (mapped to the PRD)

| PRD | Feature | Where |
|-----|---------|-------|
| P1 | Chat home — empty state, prompt suggestions, input bar | `app/(main)/page.tsx`, `components/chat/` |
| P2 | Conversation thread (deep-linkable `/c/[id]`) | `app/(main)/c/[id]/page.tsx` |
| P3 | History (grouped, deletable) | `app/(main)/history/page.tsx` |
| P6 | My Farm (location, crops, language) | `app/(main)/farm/page.tsx` |
| P7 | Settings (theme, language) | `app/(main)/settings/page.tsx` |
| F3 | Structured diagnosis card + three-tier confidence | `components/diagnosis/` |
| F7 | Source citations (expandable drawer) | `components/chat/sources-drawer.tsx` |
| F8 | Language selector | `components/shared/language-picker.tsx` |
| F23 | Feedback (thumbs up/down) | `components/chat/feedback-buttons.tsx` |
| F24 | Dark / light / system theme | `providers/theme-provider.tsx` |
| §14 | Typing indicator, confidence display, error cards | `components/chat/` |
| §15 | Full design-token system (colors, spacing, radius, shadows, motion) | `app/globals.css` |

## Deliberate deviations from the PRD (driven by the MVP backend)

The PRD describes the full product; the backend currently exposes **one
synchronous endpoint** (`POST /api/v1/query` → `{ answer, diagnosis, sources }`).
These features are therefore adapted rather than faked:

1. **No token streaming / Vercel AI SDK.** The engine returns a complete JSON
   answer, not an SSE stream. Each turn is one mutation; the typing indicator
   covers the full request. Swap in streaming when the backend supports it.
2. **Only 4 languages** (`en`, `hi`, `bn`, `as`) — the set the engine actually
   supports (`engine/knowledge_base/enums.py`), not the PRD's 7.
3. **Image & voice inputs are shown as disabled affordances** — there are no
   upload/transcription endpoints yet, so they advertise "coming soon" instead
   of breaking.
4. **History / farm profile are client-side** (localStorage). The MVP backend is
   stateless; there is no auth, conversation store, or weather service.
5. **Citations link to knowledge-base entries** (`id`, `title`, relevance score)
   with no external URL, honoring the PRD's "no hallucinated links" rule.
6. **Lightweight i18n dictionary** (`lib/i18n.ts`) instead of full next-intl, to
   keep the MVP bundle small while still centralizing all user-facing copy.

Not yet built (P1/P2 scope): onboarding flow, auth, saved responses, diagnosis
gallery, share preview, PDF export, offline queue, crop calendar.

## Verification

- `npx tsc --noEmit` — passes
- `npm run build` — passes (all routes compile)
- Verified live against the running backend: health, a successful query
  (diagnosis + sources render), and the validation-error envelope.
