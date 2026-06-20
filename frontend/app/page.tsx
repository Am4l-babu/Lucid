"use client";

import { useState, useRef } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Result = {
  text: string;
  subject: string;
  from: string;
  date: string;
};

// Gmail snippets arrive HTML-escaped (&amp;, &#39;). Decode for readability.
function decode(s: string): string {
  if (typeof document === "undefined") return s;
  const el = document.createElement("textarea");
  el.innerHTML = s;
  return el.value;
}

// "\"Amazon.in Reviews\" <x@y.com>" -> "Amazon.in Reviews"
function senderName(from: string): string {
  const m = from.match(/^\s*"?([^"<]+?)"?\s*</);
  return decode((m ? m[1] : from).trim());
}

function shortDate(date: string): string {
  const d = new Date(date);
  if (isNaN(d.getTime())) return "";
  return d.toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

type State =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "error" }
  | { kind: "done"; query: string; results: Result[] };

export default function Archive() {
  const [state, setState] = useState<State>({ kind: "idle" });
  const inputRef = useRef<HTMLInputElement>(null);

  async function search(e: React.FormEvent) {
    e.preventDefault();
    const q = inputRef.current?.value.trim();
    if (!q) return;
    setState({ kind: "loading" });
    try {
      const res = await fetch(
        `${API}/gmail/search?q=${encodeURIComponent(q)}&n=10`,
      );
      if (!res.ok) throw new Error();
      const data = await res.json();
      setState({ kind: "done", query: q, results: data.results ?? [] });
    } catch {
      setState({ kind: "error" });
    }
  }

  return (
    <main className="mx-auto flex min-h-dvh max-w-2xl flex-col px-6 py-16 sm:py-24">
      <header className="mb-16 sm:mb-24">
        <div className="flex items-baseline gap-3">
          <h1 className="font-display text-5xl font-medium leading-none tracking-tight">
            Lucid
          </h1>
          <span className="text-[0.7rem] font-medium uppercase tracking-[0.2em] text-faint">
            Archive
          </span>
        </div>
        <p className="mt-4 max-w-md text-[0.95rem] leading-relaxed text-muted">
          Search everything you&rsquo;ve written and received — by meaning, not
          keywords.
        </p>
      </header>

      <form onSubmit={search} className="group relative">
        <label htmlFor="q" className="sr-only">
          Search your archive
        </label>
        <div className="flex items-center gap-3 border-b border-ink pb-3 transition-colors focus-within:border-accent">
          <SearchGlyph className="h-5 w-5 shrink-0 text-faint transition-colors group-focus-within:text-accent" />
          <input
            id="q"
            ref={inputRef}
            type="search"
            autoComplete="off"
            autoFocus
            placeholder="a conversation, a feeling, a person&hellip;"
            className="w-full bg-transparent font-display text-2xl leading-tight text-ink outline-none placeholder:text-faint sm:text-3xl"
          />
          <button
            type="submit"
            aria-label="Search"
            className="shrink-0 cursor-pointer self-stretch px-2 text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint transition-colors hover:text-accent"
          >
            Enter
          </button>
        </div>
      </form>

      <section aria-live="polite" className="mt-12 flex-1">
        {state.kind === "loading" && <Skeleton />}
        {state.kind === "error" && (
          <Notice>
            Couldn&rsquo;t reach the archive. Is the backend running on{" "}
            <span className="tabular-nums">localhost:8000</span>?
          </Notice>
        )}
        {state.kind === "done" && state.results.length === 0 && (
          <Notice>
            Nothing matches{" "}
            <span className="text-ink">&ldquo;{state.query}&rdquo;</span> yet.
          </Notice>
        )}
        {state.kind === "done" && state.results.length > 0 && (
          <>
            <p className="mb-8 text-[0.7rem] font-medium uppercase tracking-[0.2em] text-faint">
              <span className="tabular-nums">{state.results.length}</span> result
              {state.results.length === 1 ? "" : "s"}
            </p>
            <ul className="divide-y divide-line">
              {state.results.map((r, i) => (
                <li key={i} className="group/item py-6 first:pt-0">
                  <h2 className="font-display text-xl leading-snug text-ink">
                    {decode(r.subject) || "(no subject)"}
                  </h2>
                  <p className="mt-1.5 text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint">
                    {senderName(r.from)}
                    {shortDate(r.date) && (
                      <>
                        <span className="mx-2 text-line">/</span>
                        <span className="tabular-nums normal-case tracking-normal">
                          {shortDate(r.date)}
                        </span>
                      </>
                    )}
                  </p>
                  <p className="mt-3 line-clamp-2 text-[0.95rem] leading-relaxed text-muted">
                    {decode(r.text)}
                  </p>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
    </main>
  );
}

function Notice({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-[0.95rem] leading-relaxed text-muted">{children}</p>
  );
}

function Skeleton() {
  return (
    <ul className="divide-y divide-line">
      {[0, 1, 2].map((i) => (
        <li key={i} className="py-6 first:pt-0">
          <div className="h-5 w-3/4 rounded-sm bg-line" />
          <div className="mt-3 h-3 w-1/3 rounded-sm bg-line/70" />
          <div className="mt-4 h-3.5 w-full rounded-sm bg-line/60" />
        </li>
      ))}
    </ul>
  );
}

function SearchGlyph({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-3.5-3.5" />
    </svg>
  );
}
