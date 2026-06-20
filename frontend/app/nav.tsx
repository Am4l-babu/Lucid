"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/today", label: "Today" },
  { href: "/", label: "Archive" },
  { href: "/ego", label: "Ego" },
  { href: "/drift", label: "Drift" },
  { href: "/graph", label: "Graph" },
  { href: "/relationships", label: "People" },
  { href: "/timeline", label: "Timeline" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav className="border-b border-line">
      <div className="mx-auto flex h-16 max-w-2xl items-center gap-5 px-6">
        <Link
          href="/"
          className="shrink-0 font-display text-xl font-medium tracking-tight text-ink"
        >
          Lucid
        </Link>
        <div className="flex gap-5 overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {LINKS.map((l) => {
            const active =
              l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={`shrink-0 whitespace-nowrap pb-1 text-[0.7rem] font-medium uppercase tracking-[0.2em] transition-colors ${
                  active
                    ? "border-b border-accent text-ink"
                    : "text-faint hover:text-muted"
                }`}
              >
                {l.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
