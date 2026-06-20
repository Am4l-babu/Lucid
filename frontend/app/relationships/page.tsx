"use client";

import { useState, useEffect } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Rel = { name: string; kind: string; note: string; count: number };

export default function Relationships() {
  const [state, setState] = useState<
    "loading" | "empty" | "building" | "ready" | "error"
  >("loading");
  const [rels, setRels] = useState<Rel[]>([]);

  useEffect(() => {
    fetch(`${API}/relationships`)
      .then((r) => r.json())
      .then((d) => {
        if (d.relationships?.length) {
          setRels(d.relationships);
          setState("ready");
        } else setState("empty");
      })
      .catch(() => setState("error"));
  }, []);

  async function build() {
    setState("building");
    try {
      const r = await fetch(`${API}/relationships/build`, { method: "POST" });
      if (!r.ok) throw new Error();
      const d = await r.json();
      setRels(d.relationships ?? []);
      setState("ready");
    } catch {
      setState("error");
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100dvh-4rem)] max-w-2xl flex-col px-6 py-12 sm:py-16">
      <header className="mb-12 sm:mb-16">
        <h1 className="font-display text-4xl font-medium leading-none tracking-tight text-ink sm:text-5xl">
          Relationships
        </h1>
        <p className="mt-4 max-w-md text-[0.95rem] leading-relaxed text-muted">
          Who fills your inbox, what they mean to you, and how often they reach
          out.
        </p>
      </header>

      {state === "loading" && (
        <p className="text-[0.95rem] text-faint">Loading&hellip;</p>
      )}
      {state === "error" && (
        <p className="text-[0.95rem] text-muted">
          Couldn&rsquo;t reach the backend on{" "}
          <span className="tabular-nums">localhost:8000</span>.
        </p>
      )}
      {state === "building" && (
        <p className="text-[0.95rem] text-faint">
          Reading your relationships&hellip;
        </p>
      )}

      {state === "empty" && (
        <div className="border-t border-line pt-10">
          <p className="max-w-md text-[0.95rem] leading-relaxed text-muted">
            Lucid groups your archive by person and characterises each
            relationship.
          </p>
          <button
            onClick={build}
            className="mt-7 inline-flex h-11 cursor-pointer items-center gap-2 bg-ink px-6 text-[0.8rem] font-medium uppercase tracking-[0.15em] text-paper transition-colors hover:bg-accent"
          >
            Map my relationships
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>
      )}

      {state === "ready" && (
        <>
          <ul className="divide-y divide-line border-t border-line">
            {rels.map((r, i) => (
              <li key={i} className="py-6">
                <div className="flex items-baseline justify-between gap-4">
                  <h2 className="font-display text-xl text-ink">{r.name}</h2>
                  <span className="shrink-0 text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint">
                    {r.kind}
                    <span className="mx-2 text-line">/</span>
                    <span className="tabular-nums normal-case tracking-normal">
                      {r.count} email{r.count === 1 ? "" : "s"}
                    </span>
                  </span>
                </div>
                <p className="mt-2 text-[0.95rem] leading-relaxed text-muted">
                  {r.note}
                </p>
              </li>
            ))}
          </ul>
          <button
            onClick={build}
            className="mt-8 cursor-pointer text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint transition-colors hover:text-accent"
          >
            Rebuild
          </button>
        </>
      )}
    </main>
  );
}
