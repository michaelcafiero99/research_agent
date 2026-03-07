# Morning Paper

An AI-powered deep research dashboard. Enter a topic, and a multi-step agent scouts Arxiv, Hacker News, and Semantic Scholar — streaming its progress live — then surfaces the most relevant papers scored by novelty, empirical impact, venue authority, and academic traction.

---

## Architecture

```
FastAPI backend  ──SSE──►  Next.js frontend
(research agent)           (Morning Paper UI)
```

The backend runs an agentic pipeline and streams Server-Sent Events (SSE) in two shapes:

```json
{ "type": "status",  "message": "Searching Arxiv and Semantic Scholar..." }
{ "type": "report",  "content": [ { "title": "...", "weighted_score": 8.2, ... } ] }
```

The frontend reads this stream and updates the three-pane UI in real time.

---

## Stack

| Layer | Choice |
|---|---|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS + tailwindcss-animate |
| Animation | Framer Motion |
| Icons | Lucide React |
| Fonts | Source Serif 4 (headings), JetBrains Mono (UI metadata) |
| Notifications | Sonner |

---

## UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Morning Paper                                              │
├──────────────────┬──────────────────────────┬──────────────┤
│  NEW SCOUT       │  RESEARCH CANVAS         │  EXECUTION   │
│                  │                          │  TRACE       │
│  [input]         │  Paper cards appear      │              │
│  [Scout btn]     │  here as the agent       │  ✓ Planning  │
│                  │  finds results.          │  ● Scanning  │
│                  │  Skeleton newspaper      │  ○ Consol.   │
│  DAILY ARCHIVE   │  shown before first run. │  ○ Evaluating│
│  ─────────────── │                          │  ○ Building  │
│  previous query →│                          │              │
└──────────────────┴──────────────────────────┴──────────────┘
```

---

## Getting Started

### 1. Install dependencies

```bash
yarn install
```

### 2. Configure environment

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/chat
```

Point this at your FastAPI backend endpoint. The frontend POSTs `{ "input": "<query>" }` and reads the SSE response.

### 3. Run

```bash
yarn dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Paper Scoring

Each paper returned by the backend is scored across four dimensions:

| Dimension | What it measures |
|---|---|
| **Novelty** | How new or surprising the contribution is |
| **Empirical Impact** | Strength of experimental evidence |
| **Venue Authority** | Prestige of the publication venue |
| **Academic Traction** | Citation count and community uptake |

A weighted composite score determines inclusion in the digest.

---

## Project Structure

```
app/
  globals.css        # Tailwind base, monochrome CSS vars, grain texture
  layout.tsx         # Root layout — Source Serif 4 + JetBrains Mono fonts
  page.tsx           # Mounts <AgentConsole>
components/
  AgentConsole.tsx   # Main three-pane component — all UI logic lives here
  ui/
    sonner.tsx       # Toast notifications
utils/
  cn.ts              # clsx + tailwind-merge helper
```
