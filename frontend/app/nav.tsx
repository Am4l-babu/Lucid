"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/today", label: "Today" },
  { href: "/archive", label: "Archive" },
  { href: "/ego", label: "Ego" },
  { href: "/drift", label: "Drift" },
  { href: "/graph", label: "Graph" },
  { href: "/relationships", label: "People" },
  { href: "/timeline", label: "Timeline" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <div className="pointer-events-none fixed inset-x-0 top-0 z-50 flex justify-center px-3">
      <nav className="pointer-events-auto mt-4 flex max-w-full items-center gap-3 rounded-full border border-line-2 bg-paper/60 p-1.5 pl-2.5 shadow-[0_8px_40px_-12px_rgba(0,0,0,0.7),0_0_30px_-10px_rgba(255,125,60,0.35)] backdrop-blur-2xl">
        <Link
          href="/"
          className="group flex shrink-0 items-center gap-2 pl-1"
          aria-label="Lucid — home"
        >
          <Mark />
          <span className="hidden font-display text-lg font-medium tracking-tight text-ink sm:inline">
            Lucid
          </span>
        </Link>

        <span className="h-5 w-px shrink-0 bg-line-2" aria-hidden="true" />

        {/* min-w-0 lets this scroll on mobile instead of widening the page */}
        <div className="flex min-w-0 items-center gap-0.5 overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {LINKS.map((l) => {
            const active = pathname === l.href || (l.href !== "/" && pathname.startsWith(l.href));
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={`relative shrink-0 whitespace-nowrap rounded-full px-3.5 py-2 font-mono text-[0.64rem] uppercase tracking-[0.2em] transition-colors duration-300 ${
                  active ? "text-ink" : "text-faint hover:text-muted"
                }`}
              >
                {active && (
                  <span
                    aria-hidden="true"
                    className="absolute inset-0 -z-10 rounded-full bg-surface-2 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.06),0_0_22px_-6px_rgba(255,125,60,0.6)]"
                  />
                )}
                {l.label}
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}

/* A small luminous iris — clarity / seeing yourself. */
function Mark() {
  return (
    <span className="relative grid h-7 w-7 place-items-center">
      <span className="absolute inset-0 rounded-full bg-accent/30 blur-md transition-all duration-500 group-hover:bg-accent/50" />
      <svg
        viewBox="0 0 32 32"
        className="relative h-7 w-7"
        aria-hidden="true"
        fill="none"
      >
        <circle
          cx="16"
          cy="16"
          r="13"
          stroke="var(--color-accent)"
          strokeWidth="1.4"
          opacity="0.55"
        />
        <circle cx="16" cy="16" r="6" fill="url(#irisGlow)" />
        <circle cx="13.6" cy="13.6" r="1.6" fill="#fff" opacity="0.9" />
        <defs>
          <radialGradient id="irisGlow" cx="0.4" cy="0.4" r="0.7">
            <stop offset="0" stopColor="#ffd0ad" />
            <stop offset="1" stopColor="#ff7d3c" />
          </radialGradient>
        </defs>
      </svg>
    </span>
  );
}
