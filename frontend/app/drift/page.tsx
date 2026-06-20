"use client";

import { useState, useEffect } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Align = { goal: string; status: string; note: string };

// on-track = ink, drifting = accent, stalled = faint. No banned hues.
const STATUS_CLASS: Record<string, string> = {
  "on-track": "text-ink",
  drifting: "text-accent",
  stalled: "text-faint",
};

export default function Drift() {
  const [goals, setGoals] = useState<string[]>([]);
  const [draft, setDraft] = useState("");
  const [saved, setSaved] = useState(false);
  const [checking, setChecking] = useState(false);
  const [alignment, setAlignment] = useState<Align[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`${API}/drift/goals`)
      .then((r) => r.json())
      .then((d) => setGoals(d.goals ?? []))
      .catch(() => setError(true));
  }, []);

  async function persist(next: string[]) {
    setGoals(next);
    setSaved(false);
    await fetch(`${API}/drift/goals`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goals: next }),
    });
    setSaved(true);
  }

  function add(e: React.FormEvent) {
    e.preventDefault();
    const g = draft.trim();
    if (!g) return;
    setDraft("");
    persist([...goals, g]);
  }

  function remove(i: number) {
    persist(goals.filter((_, idx) => idx !== i));
  }

  async function check() {
    setChecking(true);
    setAlignment(null);
    try {
      const r = await fetch(`${API}/drift/check`, { method: "POST" });
      if (!r.ok) throw new Error();
      const d = await r.json();
      setAlignment(d.alignment ?? []);
    } catch {
      setError(true);
    } finally {
      setChecking(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100dvh-4rem)] max-w-2xl flex-col px-6 py-12 sm:py-16">
      <header className="mb-12 sm:mb-16">
        <h1 className="font-display text-4xl font-medium leading-none tracking-tight text-ink sm:text-5xl">
          Drift
        </h1>
        <p className="mt-4 max-w-md text-[0.95rem] leading-relaxed text-muted">
          Set what matters to you. Lucid checks whether your days are actually
          moving toward it.
        </p>
      </header>

      <section>
        <h2 className="mb-5 text-[0.7rem] font-medium uppercase tracking-[0.2em] text-faint">
          Your goals
        </h2>
        {goals.length > 0 && (
          <ul className="mb-6 divide-y divide-line border-y border-line">
            {goals.map((g, i) => (
              <li key={i} className="flex items-center justify-between py-3">
                <span className="text-[0.95rem] text-ink">{g}</span>
                <button
                  onClick={() => remove(i)}
                  aria-label={`Remove goal: ${g}`}
                  className="cursor-pointer text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint transition-colors hover:text-accent"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}

        <form onSubmit={add} className="group">
          <div className="flex items-center gap-3 border-b border-ink pb-3 transition-colors focus-within:border-accent">
            <input
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="e.g. land an AI internship by August"
              className="w-full bg-transparent font-display text-xl leading-tight text-ink outline-none placeholder:text-faint sm:text-2xl"
            />
            <button
              type="submit"
              className="shrink-0 cursor-pointer px-2 text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint transition-colors hover:text-accent"
            >
              Add
            </button>
          </div>
        </form>
        {saved && (
          <p className="mt-3 text-[0.7rem] uppercase tracking-[0.15em] text-faint">
            Saved
          </p>
        )}
      </section>

      {goals.length > 0 && (
        <section className="mt-12">
          <button
            onClick={check}
            disabled={checking}
            className="inline-flex h-11 cursor-pointer items-center gap-2 bg-ink px-6 text-[0.8rem] font-medium uppercase tracking-[0.15em] text-paper transition-colors hover:bg-accent disabled:cursor-default disabled:bg-faint"
          >
            {checking ? "Checking…" : "Check my drift"}
            {!checking && <span aria-hidden="true">&rarr;</span>}
          </button>

          {alignment && (
            <div className="mt-10 border-t border-line" aria-live="polite">
              {alignment.map((a, i) => (
                <div key={i} className="border-b border-line py-6">
                  <div className="flex items-baseline justify-between gap-4">
                    <h3 className="text-[0.95rem] text-ink">{a.goal}</h3>
                    <span
                      className={`shrink-0 text-[0.7rem] font-medium uppercase tracking-[0.15em] ${
                        STATUS_CLASS[a.status] ?? "text-muted"
                      }`}
                    >
                      {a.status}
                    </span>
                  </div>
                  <p className="mt-2 text-[0.9rem] leading-relaxed text-muted">
                    {a.note}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      {error && (
        <p className="mt-8 text-[0.95rem] text-muted">
          Couldn&rsquo;t reach the backend on{" "}
          <span className="tabular-nums">localhost:8000</span>.
        </p>
      )}
    </main>
  );
}
