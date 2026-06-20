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
    <nav className="sticky top-0 z-10 border-b border-line bg-paper/90 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-2xl items-center px-6">
        <Link
          href="/"
          className="mr-8 shrink-0 font-display text-xl font-medium tracking-tight text-ink"
        >
          Lucid
        </Link>
        {/* min-w-0 lets this actually scroll instead of widening the page */}
        <div className="flex min-w-0 flex-1 gap-7 overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {LINKS.map((l) => {
            const active =
              l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={`shrink-0 whitespace-nowrap py-1 text-[0.7rem] font-medium uppercase tracking-[0.15em] transition-colors ${
                  active
                    ? "text-accent"
                    : "text-faint hover:text-ink"
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
