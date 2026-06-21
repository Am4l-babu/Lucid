"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";

/* template.tsx re-mounts on every navigation, so this runs a fresh entrance
   on each route change: a quick clip-path wipe overlay clears downward while
   the page fades up beneath it. */
export default function Template({ children }: { children: React.ReactNode }) {
  const pageRef = useRef<HTMLDivElement>(null);
  const wipeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const reduced =
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
    if (wipeRef.current) {
      tl.set(wipeRef.current, {
        clipPath: "inset(0% 0% 0% 0%)",
        opacity: 1,
      }).to(wipeRef.current, {
        clipPath: "inset(0% 0% 100% 0%)",
        duration: 0.7,
        ease: "power4.inOut",
      });
    }
    if (pageRef.current) {
      tl.from(
        pageRef.current,
        { opacity: 0, y: 22, duration: 0.7, clearProps: "opacity,transform" },
        0.15,
      );
    }
    return () => {
      // Complete the timeline before killing so inline styles are cleared
      tl.progress(1);
      tl.kill();
    };
  }, []);

  return (
    <>
      <div
        ref={wipeRef}
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 z-40 opacity-0"
        style={{
          background:
            "linear-gradient(180deg, #15110e, #0c0a09)",
          clipPath: "inset(0% 0% 100% 0%)",
        }}
      />
      <div ref={pageRef}>{children}</div>
    </>
  );
}
