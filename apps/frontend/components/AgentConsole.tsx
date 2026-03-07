"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Check, Search, ExternalLink, ArrowRight } from "lucide-react";
import { cn } from "@/utils/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

type StageStatus = "pending" | "running" | "done";

type StageDefinition = {
  id: string;
  label: string;
  keywords: string[];
};

type Stage = StageDefinition & { status: StageStatus };

type Paper = {
  title: string;
  url: string;
  novelty_score: number;
  empirical_impact_score: number;
  venue_authority_score: number;
  academic_traction_score: number;
  weighted_score: number;
  include_in_digest: boolean;
  reasoning: string;
};

// ─── Stage config ─────────────────────────────────────────────────────────────

const STAGE_DEFS: StageDefinition[] = [
  { id: "planning",      label: "Planning Strategy",      keywords: ["strateg"] },
  { id: "scanning",      label: "Scanning Sources",       keywords: ["search", "arxiv", "semantic"] },
  { id: "consolidating", label: "Consolidating Research", keywords: ["consolidat"] },
  { id: "evaluating",    label: "Evaluating Relevance",   keywords: ["scor", "evaluat"] },
  { id: "building",      label: "Building Digest",        keywords: ["build", "digest"] },
];

function freshStages(): Stage[] {
  return STAGE_DEFS.map((d) => ({ ...d, status: "pending" }));
}

function matchStageIndex(msg: string): number {
  const lower = msg.toLowerCase();
  for (let i = 0; i < STAGE_DEFS.length; i++) {
    if (STAGE_DEFS[i].keywords.some((k) => lower.includes(k))) return i;
  }
  return -1;
}

// ─── Bento primitives ─────────────────────────────────────────────────────────

function BentoCard({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("bg-white overflow-hidden", className)}>
      {children}
    </div>
  );
}

// ─── Newspaper skeleton ───────────────────────────────────────────────────────

function NewspaperSkeleton() {
  return (
    <div className="h-full flex flex-col items-center justify-center select-none">
      <svg
        viewBox="0 0 420 260"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-72 opacity-[0.18]"
        aria-hidden="true"
      >
        {/* Outer border */}
        <rect x="1" y="1" width="418" height="258" rx="2" stroke="#71717a" strokeWidth="1" />
        {/* Spine */}
        <line x1="210" y1="12" x2="210" y2="248" stroke="#71717a" strokeWidth="0.75" />
        {/* Date line */}
        <rect x="16" y="12" width="60" height="5" rx="1" fill="#d4d4d8" />
        <rect x="344" y="12" width="60" height="5" rx="1" fill="#d4d4d8" />
        {/* Headline bar */}
        <rect x="16" y="28" width="174" height="14" rx="1" fill="#a1a1aa" />
        <rect x="16" y="46" width="130" height="9" rx="1" fill="#d4d4d8" />
        {/* Divider */}
        <line x1="16" y1="64" x2="194" y2="64" stroke="#e4e4e7" strokeWidth="0.75" />
        {/* Left col – body lines */}
        {[76,88,100,112,124,136,148,160,172,184,196,208,220,232].map((y) => (
          <rect key={y} x="16" y={y} width={y % 40 === 0 ? 140 : 174} height="6" rx="1" fill="#e4e4e7" />
        ))}
        {/* Right col – headline */}
        <rect x="224" y="28" width="174" height="14" rx="1" fill="#a1a1aa" />
        <rect x="224" y="46" width="110" height="9" rx="1" fill="#d4d4d8" />
        {/* Right col – sub-image placeholder */}
        <rect x="224" y="64" width="174" height="56" rx="1" fill="#f4f4f5" />
        {/* Right col – body lines */}
        {[130,142,154,166,178,190,202,214,226,238].map((y) => (
          <rect key={y} x="224" y={y} width={y % 36 === 0 ? 130 : 174} height="6" rx="1" fill="#e4e4e7" />
        ))}
      </svg>
      <p className="font-serif-display text-2xl text-zinc-300 mt-6 tracking-tight">
        Start a scout
      </p>
      <p className="font-mono-ui text-[11px] text-zinc-300 mt-1.5 tracking-wide">
        Enter a research topic to begin
      </p>
    </div>
  );
}

// ─── Scanning skeleton ────────────────────────────────────────────────────────

function ScanSkeleton() {
  return (
    <div className="space-y-4">
      {[...Array(3)].map((_, i) => (
        <div
          key={i}
          className="border border-zinc-100 p-5 animate-pulse"
          style={{ animationDelay: `${i * 150}ms` }}
        >
          <div className="flex justify-between items-start mb-3">
            <div className="space-y-1.5 flex-1">
              <div className="h-3 bg-zinc-100 rounded w-4/5" />
              <div className="h-3 bg-zinc-100 rounded w-3/5" />
            </div>
            <div className="h-5 w-10 bg-zinc-100 rounded-full ml-4 shrink-0" />
          </div>
          <div className="h-px bg-zinc-50 my-3" />
          <div className="space-y-1.5">
            <div className="h-2.5 bg-zinc-50 rounded w-full" />
            <div className="h-2.5 bg-zinc-50 rounded w-5/6" />
          </div>
          <div className="h-px bg-zinc-50 my-3" />
          <div className="grid grid-cols-2 gap-x-4 gap-y-2">
            {[...Array(4)].map((_, j) => (
              <div key={j} className="flex items-center gap-2">
                <div className="h-2 bg-zinc-100 rounded w-10 shrink-0" />
                <div className="flex-1 h-px bg-zinc-100" />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

// ─── Paper Bento Card ─────────────────────────────────────────────────────────

function ScoreRow({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex items-center gap-2.5">
      <span className="font-mono-ui text-[9px] uppercase tracking-widest text-zinc-400 w-12 shrink-0">
        {label}
      </span>
      <div className="flex-1 h-px bg-zinc-100 relative overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 bg-zinc-800"
          initial={{ width: 0 }}
          animate={{ width: `${(value / 10) * 100}%` }}
          transition={{ duration: 0.8, ease: "easeOut", delay: 0.2 }}
        />
      </div>
      <span className="font-mono-ui text-[10px] text-zinc-400 tabular-nums w-4 text-right">
        {value.toFixed(0)}
      </span>
    </div>
  );
}

function extractDomain(url: string): string {
  try {
    const u = new URL(url);
    return u.hostname.replace("www.", "");
  } catch {
    return url;
  }
}

function PaperBentoCard({ paper }: { paper: Paper }) {
  return (
    <div className="border border-zinc-200 bg-white hover:shadow-[0_12px_36px_rgba(0,0,0,0.07)] transition-shadow duration-300 group">
      {/* Header row: source label + score badge */}
      <div className="px-5 pt-4 pb-3 flex items-start justify-between gap-3 border-b border-zinc-50">
        <span className="font-mono-ui text-[9px] uppercase tracking-widest text-zinc-400 mt-0.5">
          Relevance Score
        </span>
        <span className="font-mono-ui text-xs font-medium bg-zinc-900 text-white px-2.5 py-0.5 rounded-full tabular-nums shrink-0">
          {paper.weighted_score.toFixed(1)}
        </span>
      </div>

      {/* Title + citation */}
      <div className="px-5 py-4 border-b border-zinc-50">
        <h3 className="font-serif-display text-[15px] leading-snug text-zinc-900 mb-2 group-hover:text-zinc-700 transition-colors">
          {paper.title}
        </h3>
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 font-mono-ui text-[10px] text-zinc-400 hover:text-zinc-900 transition-colors"
        >
          <span>{extractDomain(paper.url)}</span>
          <ExternalLink className="w-2.5 h-2.5" />
        </a>
      </div>

      {/* Reasoning */}
      <div className="px-5 py-3 border-b border-zinc-50">
        <p className="text-xs text-zinc-500 leading-relaxed">{paper.reasoning}</p>
      </div>

      {/* Score metrics */}
      <div className="px-5 py-3 grid grid-cols-2 gap-x-6 gap-y-2">
        <ScoreRow label="Novelty"  value={paper.novelty_score} />
        <ScoreRow label="Impact"   value={paper.empirical_impact_score} />
        <ScoreRow label="Venue"    value={paper.venue_authority_score} />
        <ScoreRow label="Traction" value={paper.academic_traction_score} />
      </div>

      {/* Source citation footer */}
      <div className="px-5 py-2.5 bg-zinc-50 border-t border-zinc-100 flex items-center justify-between">
        <span className="font-mono-ui text-[9px] text-zinc-400 uppercase tracking-widest">
          Source
        </span>
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="font-mono-ui text-[10px] text-zinc-500 hover:text-zinc-900 truncate max-w-[240px] transition-colors"
        >
          {paper.url}
        </a>
      </div>
    </div>
  );
}

// ─── Execution Trace ──────────────────────────────────────────────────────────

function ExecutionTrace({
  stages,
  currentStatusMessage,
}: {
  stages: Stage[];
  currentStatusMessage: string;
}) {
  return (
    <div className="relative pl-6">
      {/* Vertical connecting line */}
      <div className="absolute left-[7px] top-2 bottom-2 w-px bg-zinc-100" />

      <div className="space-y-6">
        {stages.map((stage) => (
          <div key={stage.id} className="relative">
            {/* Node */}
            <div className="absolute -left-6 top-0.5 z-10">
              {stage.status === "done" && (
                <div className="w-4 h-4 rounded-full bg-zinc-900 flex items-center justify-center">
                  <Check className="w-2.5 h-2.5 text-white stroke-[3]" />
                </div>
              )}
              {stage.status === "running" && (
                <motion.div
                  className="w-3.5 h-3.5 rounded-full bg-zinc-900"
                  animate={{ scale: [1, 1.35, 1], opacity: [1, 0.6, 1] }}
                  transition={{ duration: 1.4, repeat: Infinity, ease: "easeInOut" }}
                />
              )}
              {stage.status === "pending" && (
                <div className="w-2.5 h-2.5 rounded-full border border-zinc-200 bg-white mt-0.5 ml-0.5" />
              )}
            </div>

            {/* Label */}
            <p
              className={cn(
                "font-mono-ui text-[11px] leading-none transition-colors duration-300",
                stage.status === "pending" && "text-zinc-300",
                stage.status === "running" && "text-zinc-900 font-medium",
                stage.status === "done"    && "text-zinc-400",
              )}
            >
              {stage.label}
            </p>

            {/* Real-time status sub-text for active step */}
            {stage.status === "running" && (
              <AnimatePresence mode="wait">
                <motion.p
                  key={currentStatusMessage}
                  initial={{ opacity: 0, y: 3 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -3 }}
                  transition={{ duration: 0.25 }}
                  className="font-mono-ui text-[9px] text-zinc-400 mt-1.5 leading-relaxed"
                >
                  {currentStatusMessage}
                </motion.p>
              </AnimatePresence>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Daily Archive ────────────────────────────────────────────────────────────

function DailyArchive({
  items,
  isRunning,
  onSelect,
}: {
  items: string[];
  isRunning: boolean;
  onSelect: (q: string) => void;
}) {
  if (items.length === 0) return null;
  return (
    <div className="border-t border-zinc-100 pt-4 pb-4 px-5">
      <p className="font-mono-ui text-[9px] uppercase tracking-widest text-zinc-400 mb-3">
        Daily Archive
      </p>
      <div className="flex flex-col">
        {items.map((item, i) => (
          <button
            key={i}
            onClick={() => onSelect(item)}
            disabled={isRunning}
            className={cn(
              "group w-full text-left border border-zinc-200 bg-white px-3 py-2.5",
              "-mt-px first:mt-0",
              "hover:z-10 hover:relative hover:border-zinc-400 hover:bg-zinc-50",
              "transition-colors duration-150 disabled:opacity-30",
            )}
          >
            <div className="flex items-center justify-between gap-2">
              <span className="font-mono-ui text-[11px] text-zinc-500 group-hover:text-zinc-900 truncate transition-colors">
                {item}
              </span>
              <ArrowRight className="w-3 h-3 text-zinc-300 group-hover:text-zinc-600 shrink-0 transition-colors" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export function AgentConsole({ endpoint }: { endpoint: string }) {
  const [query, setQuery]                       = useState("");
  const [stages, setStages]                     = useState<Stage[]>(freshStages);
  const [papers, setPapers]                     = useState<Paper[]>([]);
  const [isRunning, setIsRunning]               = useState(false);
  const [hasRun, setHasRun]                     = useState(false);
  const [currentStatusMessage, setCurrentStatusMessage] = useState("");
  const [previousScouts, setPreviousScouts]     = useState<string[]>([]);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    try {
      const s = localStorage.getItem("scout-history");
      if (s) setPreviousScouts(JSON.parse(s));
    } catch {}
  }, []);

  const saveToHistory = useCallback((q: string) => {
    setPreviousScouts((prev) => {
      const next = [q, ...prev.filter((h) => h !== q)].slice(0, 10);
      try { localStorage.setItem("scout-history", JSON.stringify(next)); } catch {}
      return next;
    });
  }, []);

  const runScout = useCallback(
    async (q: string) => {
      if (!q.trim() || isRunning) return;

      setStages(freshStages());
      setPapers([]);
      setCurrentStatusMessage("");
      setIsRunning(true);
      setHasRun(true);
      saveToHistory(q);

      abortRef.current?.abort();
      abortRef.current = new AbortController();

      let currentStageIdx = -1;

      const advanceStage = (newIdx: number) => {
        if (newIdx <= currentStageIdx) return; // never go backward or repeat
        // Mark every stage before newIdx as done (handles skipped stages),
        // and mark newIdx as running in a single state update.
        setStages((p) =>
          p.map((s, i) => {
            if (i < newIdx)  return { ...s, status: "done" };
            if (i === newIdx) return { ...s, status: "running" };
            return s;
          }),
        );
        currentStageIdx = newIdx;
      };

      try {
        const url = endpoint;
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input: q }),
          signal: abortRef.current.signal,
        });
        if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);

        const reader  = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer    = "";

        outer: while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop() ?? "";

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const raw = line.slice(6).trim();
            if (raw === "[DONE]") break outer;

            try {
              const event = JSON.parse(raw);
              if (event.type === "status" && typeof event.message === "string") {
                setCurrentStatusMessage(event.message);
                const idx = matchStageIndex(event.message);
                if (idx !== -1) advanceStage(idx);
              } else if (event.type === "report" && Array.isArray(event.content)) {
                setStages((p) => p.map((s) => ({ ...s, status: "done" })));
                setCurrentStatusMessage("");
                setPapers(event.content.filter((p: Paper) => p.include_in_digest !== false));
              }
            } catch { /* skip malformed */ }
          }
        }

        setStages((p) => p.map((s) => s.status === "running" ? { ...s, status: "done" } : s));
        setCurrentStatusMessage("");
      } catch (err: any) {
        if (err.name !== "AbortError") console.error("Scout error:", err);
      } finally {
        setIsRunning(false);
      }
    },
    [isRunning, endpoint, saveToHistory],
  );

  return (
    <div className="absolute inset-0 flex overflow-hidden bg-white">

      {/* ── Left Bento Card: Controls ──────────────────────────────────── */}
      <BentoCard className="w-72 shrink-0 flex flex-col border-r border-zinc-100 bg-[#F9F9F9]">

        <div className="px-5 pt-5 pb-4 border-b border-zinc-100">
          <p className="font-mono-ui text-[9px] uppercase tracking-widest text-zinc-400 mb-3">
            New Scout
          </p>
          <form
            onSubmit={(e) => { e.preventDefault(); runScout(query); }}
            className="space-y-2"
          >
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-400 pointer-events-none" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Research topic…"
                disabled={isRunning}
                aria-label="Research topic"
                className="w-full pl-9 pr-3 py-2.5 text-sm bg-white border-2 border-zinc-900 outline-none placeholder:text-zinc-300 disabled:opacity-50 focus:border-zinc-900 font-sans"
              />
            </div>
            <button
              type="submit"
              disabled={isRunning || !query.trim()}
              aria-label="Start scout"
              className="w-full py-2.5 text-sm font-medium bg-zinc-900 text-white hover:bg-zinc-700 active:bg-zinc-800 transition-colors disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isRunning ? (
                <motion.span
                  className="inline-block w-3 h-3 border-2 border-white/30 border-t-white rounded-full"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 0.8, repeat: Infinity, ease: "linear" }}
                />
              ) : (
                <Search className="w-3.5 h-3.5" />
              )}
              Scout
            </button>
          </form>
        </div>

        <div className="flex-1" />

        <DailyArchive
          items={previousScouts}
          isRunning={isRunning}
          onSelect={(q) => { setQuery(q); runScout(q); }}
        />
      </BentoCard>

      {/* ── Center Bento Card: Canvas ───────────────────────────────────── */}
      <BentoCard className="flex-1 flex flex-col overflow-hidden min-w-0 border-r border-zinc-100">

        <div className="border-b border-zinc-100 px-7 py-4 flex items-center justify-between shrink-0">
          <span className="font-mono-ui text-[9px] uppercase tracking-widest text-zinc-400">
            Research Canvas
          </span>
          {papers.length > 0 && (
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="font-mono-ui text-[9px] text-zinc-400 tabular-nums"
            >
              {papers.length} paper{papers.length !== 1 ? "s" : ""}
            </motion.span>
          )}
        </div>

        <div className="flex-1 overflow-y-auto p-7">
          {!hasRun && <NewspaperSkeleton />}
          {isRunning && papers.length === 0 && <ScanSkeleton />}

          {papers.length > 0 && (
            <div
              className={cn(
                "grid gap-4",
                papers.length > 1 ? "grid-cols-2" : "grid-cols-1",
              )}
            >
              <AnimatePresence>
                {papers.map((paper, i) => (
                  <motion.div
                    key={paper.url}
                    initial={{ opacity: 0, y: 24, scale: 0.97 }}
                    animate={{ opacity: 1, y: 0,  scale: 1 }}
                    transition={{
                      type: "spring",
                      stiffness: 280,
                      damping: 22,
                      delay: i * 0.07,
                    }}
                  >
                    <PaperBentoCard paper={paper} />
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          )}
        </div>
      </BentoCard>

      {/* ── Right Bento Card: Execution Trace ──────────────────────────── */}
      <BentoCard className="w-56 shrink-0 flex flex-col bg-[#F9F9F9]">
        <div className="px-5 pt-5 pb-4 border-b border-zinc-100">
          <p className="font-mono-ui text-[9px] uppercase tracking-widest text-zinc-400">
            Execution Trace
          </p>
        </div>
        <div className="p-5 flex-1">
          <ExecutionTrace stages={stages} currentStatusMessage={currentStatusMessage} />
        </div>
      </BentoCard>
    </div>
  );
}
