"use client";

import { useState, useEffect } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Theme = { title: string; detail: string };
type Insights = {
  generated: boolean;
  generated_at?: string;
  sample_size?: number;
  summary?: string;
  themes?: Theme[];
};

type State =
  | { kind: "loading" }
  | { kind: "empty" }
  | { kind: "generating" }
  | { kind: "error" }
  | { kind: "done"; data: Insights };

export default function Ego() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    fetch(`${API}/ego/insights`)
      .then((r) => r.json())
      .then((d: Insights) =>
        setState(d.generated ? { kind: "done", data: d } : { kind: "empty" }),
      )
      .catch(() => setState({ kind: "error" }));
  }, []);

  async function analyze() {
    setState({ kind: "generating" });
    try {
      const r = await fetch(`${API}/ego/analyze`, { method: "POST" });
      if (!r.ok) throw new Error();
      setState({ kind: "done", data: await r.json() });
    } catch {
      setState({ kind: "error" });
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100dvh-4rem)] max-w-2xl flex-col px-6 py-12 sm:py-16">
      <header className="mb-12 sm:mb-16">
        <h1 className="font-display text-4xl font-medium leading-none tracking-tight text-ink sm:text-5xl">
          Ego
        </h1>
        <p className="mt-4 max-w-md text-[0.95rem] leading-relaxed text-muted">
          What your archive says about you — themes, attention, and the texture
          of your days.
        </p>
      </header>

      {state.kind === "loading" && (
        <p className="text-[0.95rem] text-faint">Loading&hellip;</p>
      )}

      {state.kind === "error" && (
        <p className="text-[0.95rem] leading-relaxed text-muted">
          Couldn&rsquo;t reach the archive. Is the backend running on{" "}
          <span className="tabular-nums">localhost:8000</span>?
        </p>
      )}

      {state.kind === "empty" && (
        <div className="border-t border-line pt-10">
          <p className="max-w-md text-[0.95rem] leading-relaxed text-muted">
            Ego reads across your archive to surface the patterns you can&rsquo;t
            see from a single message.
          </p>
          <button
            onClick={analyze}
            className="mt-7 inline-flex h-11 cursor-pointer items-center gap-2 bg-ink px-6 text-[0.8rem] font-medium uppercase tracking-[0.15em] text-paper transition-colors hover:bg-accent"
          >
            Analyze my archive
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>
      )}

      {state.kind === "generating" && (
        <p className="text-[0.95rem] text-faint">
          Reading across your archive&hellip; this takes a moment.
        </p>
      )}

      {state.kind === "done" && <Report data={state.data} onRerun={analyze} />}
    </main>
  );
}

function Report({ data, onRerun }: { data: Insights; onRerun: () => void }) {
  return (
    <div>
      <p className="font-display text-2xl leading-relaxed text-ink">
        {data.summary}
      </p>

      <div className="mt-14 border-t border-line">
        {(data.themes ?? []).map((t, i) => (
          <div key={i} className="border-b border-line py-6">
            <h2 className="text-[0.7rem] font-medium uppercase tracking-[0.2em] text-accent">
              {t.title}
            </h2>
            <p className="mt-2 text-[0.95rem] leading-relaxed text-ink">
              {t.detail}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-10 flex items-center gap-4">
        <button
          onClick={onRerun}
          className="cursor-pointer text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint transition-colors hover:text-accent"
        >
          Re-analyze
        </button>
        {data.sample_size && (
          <span className="text-[0.7rem] uppercase tracking-[0.15em] text-faint">
            <span className="tabular-nums">{data.sample_size}</span> emails read
          </span>
        )}
      </div>
    </div>
  );
}
