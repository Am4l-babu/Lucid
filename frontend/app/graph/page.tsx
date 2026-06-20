"use client";

import { useState, useEffect, useRef } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const COLORS = {
  paper: "#faf8f4",
  ink: "#1b1714",
  accent: "#b4470f",
  faint: "#9b938a",
  line: "#e7e1d8",
};

type Node = {
  id: string;
  label: string;
  type: "person" | "topic";
  weight?: number;
};
type Edge = { source: string; target: string };
type Graph = { generated?: boolean; nodes: Node[]; edges: Edge[] };

type Sim = Node & { x: number; y: number; vx: number; vy: number; r: number };

export default function GraphPage() {
  const [state, setState] = useState<
    "loading" | "empty" | "building" | "ready" | "error"
  >("loading");
  const [graph, setGraph] = useState<Graph | null>(null);

  useEffect(() => {
    fetch(`${API}/graph`)
      .then((r) => r.json())
      .then((g: Graph) => {
        if (g.nodes?.length) {
          setGraph(g);
          setState("ready");
        } else setState("empty");
      })
      .catch(() => setState("error"));
  }, []);

  async function build() {
    setState("building");
    try {
      const r = await fetch(`${API}/graph/build`, { method: "POST" });
      if (!r.ok) throw new Error();
      const g = await r.json();
      setGraph(g);
      setState("ready");
    } catch {
      setState("error");
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100dvh-4rem)] max-w-4xl flex-col px-6 py-12 sm:py-16">
      <header className="mb-8">
        <h1 className="font-display text-4xl font-medium leading-none tracking-tight text-ink sm:text-5xl">
          Constellation
        </h1>
        <p className="mt-4 max-w-md text-[0.95rem] leading-relaxed text-muted">
          The people and themes in your archive, and how they connect.
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
          Mapping your archive&hellip; this takes a moment.
        </p>
      )}
      {state === "empty" && (
        <div className="border-t border-line pt-10">
          <p className="max-w-md text-[0.95rem] leading-relaxed text-muted">
            Build a living map of who and what fills your archive.
          </p>
          <button
            onClick={build}
            className="mt-7 inline-flex h-11 cursor-pointer items-center gap-2 bg-ink px-6 text-[0.8rem] font-medium uppercase tracking-[0.15em] text-paper transition-colors hover:bg-accent"
          >
            Build constellation
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>
      )}

      {state === "ready" && graph && (
        <>
          <Constellation graph={graph} />
          <div className="mt-6 flex items-center gap-6">
            <Legend color={COLORS.ink} label="People" />
            <Legend color={COLORS.accent} label="Themes" />
            <button
              onClick={build}
              className="ml-auto cursor-pointer text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint transition-colors hover:text-accent"
            >
              Rebuild
            </button>
          </div>
        </>
      )}
    </main>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span className="flex items-center gap-2 text-[0.7rem] font-medium uppercase tracking-[0.15em] text-faint">
      <span
        className="h-2 w-2 rounded-full"
        style={{ backgroundColor: color }}
        aria-hidden="true"
      />
      {label}
    </span>
  );
}

function Constellation({ graph }: { graph: Graph }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const hoverRef = useRef<string | null>(null);
  const selectedRef = useRef<string | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d")!;
    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    let W = 0;
    let H = 0;
    const dpr = window.devicePixelRatio || 1;

    function resize() {
      const rect = canvas!.getBoundingClientRect();
      W = rect.width;
      H = rect.height;
      canvas!.width = W * dpr;
      canvas!.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();

    // Scatter nodes across a disc so they settle organically, not on a ring.
    const nodes: Sim[] = graph.nodes.map((n, i) => {
      const a = (i / graph.nodes.length) * Math.PI * 2 + Math.random();
      const rad = 20 + Math.random() * 90;
      return {
        ...n,
        x: W / 2 + Math.cos(a) * rad,
        y: H / 2 + Math.sin(a) * rad,
        vx: 0,
        vy: 0,
        r: 5 + Math.min(10, n.weight ?? 3) * 1.1,
      };
    });
    const byId = new Map(nodes.map((n) => [n.id, n]));
    const edges = graph.edges
      .map((e) => ({ a: byId.get(e.source), b: byId.get(e.target) }))
      .filter((e): e is { a: Sim; b: Sim } => !!e.a && !!e.b);

    const neighbours = new Map<string, Set<string>>();
    edges.forEach(({ a, b }) => {
      (neighbours.get(a.id) ?? neighbours.set(a.id, new Set()).get(a.id)!).add(b.id);
      (neighbours.get(b.id) ?? neighbours.set(b.id, new Set()).get(b.id)!).add(a.id);
    });

    // Everything scales to canvas width so it looks right on phone and desktop.
    const scaleNow = () => Math.max(0.55, Math.min(1, W / 720));
    const baseR = (n: Sim) => 5 + Math.min(10, n.weight ?? 3) * 1.1;

    function step() {
      const cx = W / 2;
      const cy = H / 2;
      const scale = scaleNow();
      // round cluster region, with margin reserved for node + label
      const R = Math.min(W, H) / 2 - (44 * scale + 22);
      const MAX = 6;

      // When a node is focused (tapped/clicked), its neighbourhood spreads out
      // for readability and everything unrelated eases to the periphery.
      const focus = selectedRef.current;
      const fNbrs = focus ? neighbours.get(focus) : null;
      // stronger repulsion while focused so labels/lines stop overlapping
      const repel = (focus ? 1500 : 700) * scale;

      for (const n of nodes) {
        n.r = baseR(n) * scale;
        let fx = 0;
        let fy = 0;
        for (const m of nodes) {
          if (m === n) continue;
          const dx = n.x - m.x;
          const dy = n.y - m.y;
          const d2 = dx * dx + dy * dy + 0.01;
          const f = Math.min(focus ? 60 : 30, repel / d2);
          fx += f * dx;
          fy += f * dy;
        }
        if (focus) {
          if (n.id === focus) {
            fx += (cx - n.x) * 0.16;
            fy += (cy - n.y) * 0.16;
          } else if (fNbrs?.has(n.id)) {
            fx += (cx - n.x) * 0.015;
            fy += (cy - n.y) * 0.015;
          } else {
            // push the unrelated nodes outward, out of the way
            const dx = n.x - cx;
            const dy = n.y - cy;
            const d = Math.hypot(dx, dy) || 0.01;
            fx += (dx / d) * 1.6 + (cx - n.x) * 0.004;
            fy += (dy / d) * 1.6 + (cy - n.y) * 0.004;
          }
        } else {
          // firm pull to centre keeps it a clump, not a scatter
          fx += (cx - n.x) * 0.045 + (Math.random() - 0.5) * 0.2 * scale;
          fy += (cy - n.y) * 0.045 + (Math.random() - 0.5) * 0.2 * scale;
        }
        n.vx = (n.vx + fx) * 0.86;
        n.vy = (n.vy + fy) * 0.86;
      }
      for (const { a, b } of edges) {
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.hypot(dx, dy) || 0.01;
        // focused node's edges sit longer so its neighbours fan out around it
        const touchesFocus = focus && (a.id === focus || b.id === focus);
        const rest = (touchesFocus ? 120 : 64) * scale;
        const diff = (d - rest) * 0.04;
        const ux = dx / d;
        const uy = dy / d;
        a.vx += ux * diff;
        a.vy += uy * diff;
        b.vx -= ux * diff;
        b.vy -= uy * diff;
      }
      for (const n of nodes) {
        // clamp speed so a node can never get launched off-screen
        const sp = Math.hypot(n.vx, n.vy);
        if (sp > MAX) {
          n.vx = (n.vx / sp) * MAX;
          n.vy = (n.vy / sp) * MAX;
        }
        n.x += n.vx;
        n.y += n.vy;
        // hard circular boundary — nothing ever leaves the disc
        const dx = n.x - cx;
        const dy = n.y - cy;
        const dist = Math.hypot(dx, dy) || 0.01;
        const limit = R - n.r;
        if (dist > limit) {
          n.x = cx + (dx / dist) * limit;
          n.y = cy + (dy / dist) * limit;
          n.vx *= -0.3;
          n.vy *= -0.3;
        }
      }
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      const hovered = selectedRef.current ?? hoverRef.current;
      const near = hovered ? neighbours.get(hovered) : null;
      const scale = scaleNow();
      const fontPx = Math.max(9, Math.round(11 * scale));
      const maxLabel = scale < 0.72 ? 11 : 16;
      const trim = (s: string) =>
        s.length > maxLabel ? s.slice(0, maxLabel - 1).trimEnd() + "…" : s;

      // edges
      for (const { a, b } of edges) {
        const active = hovered && (a.id === hovered || b.id === hovered);
        ctx.globalAlpha = active ? 0.9 : hovered ? 0.12 : 0.38;
        ctx.strokeStyle = active ? COLORS.accent : COLORS.faint;
        ctx.lineWidth = active ? 1.3 : 0.7;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
      ctx.globalAlpha = 1;

      // nodes + labels
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      for (const n of nodes) {
        const isPerson = n.type === "person";
        const color = isPerson ? COLORS.ink : COLORS.accent;
        const focused = !hovered || n.id === hovered || near?.has(n.id);
        ctx.globalAlpha = focused ? 1 : 0.25;

        ctx.shadowColor = color;
        ctx.shadowBlur = (n.id === hovered ? 22 : focused ? 11 : 0) * scale;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.shadowBlur = 0;

        if (isPerson) {
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.r + 3 * scale, 0, Math.PI * 2);
          ctx.strokeStyle = color;
          ctx.globalAlpha = focused ? 0.25 : 0.1;
          ctx.lineWidth = 1;
          ctx.stroke();
          ctx.globalAlpha = focused ? 1 : 0.25;
        }

        ctx.font = `${isPerson ? 600 : 500} ${fontPx}px "Hanken Grotesk", sans-serif`;
        ctx.fillStyle = color;
        ctx.fillText(trim(n.label), n.x, n.y + n.r + fontPx);
        ctx.globalAlpha = 1;
      }
    }

    let raf = 0;
    let ticks = 0;
    function loop() {
      step();
      draw();
      ticks++;
      // Reduced motion: settle quickly then hold.
      if (!(reduced && ticks > 120)) raf = requestAnimationFrame(loop);
    }
    loop();

    function nodeAt(clientX: number, clientY: number): string | null {
      const rect = canvas!.getBoundingClientRect();
      const mx = clientX - rect.left;
      const my = clientY - rect.top;
      for (const n of nodes) {
        if ((mx - n.x) ** 2 + (my - n.y) ** 2 < (n.r + 10) ** 2) return n.id;
      }
      return null;
    }

    function onMove(e: MouseEvent) {
      const found = nodeAt(e.clientX, e.clientY);
      hoverRef.current = found;
      canvas!.style.cursor = found ? "pointer" : "default";
      if (reduced) draw();
    }

    // Tap / click a node to focus it (toggles); tapping empty space clears.
    function onTap(e: PointerEvent) {
      const found = nodeAt(e.clientX, e.clientY);
      selectedRef.current = selectedRef.current === found ? null : found;
      if (reduced) draw();
    }

    canvas.addEventListener("mousemove", onMove);
    canvas.addEventListener("pointerdown", onTap);
    window.addEventListener("resize", resize);

    return () => {
      cancelAnimationFrame(raf);
      canvas.removeEventListener("mousemove", onMove);
      canvas.removeEventListener("pointerdown", onTap);
      window.removeEventListener("resize", resize);
    };
  }, [graph]);

  return (
    <canvas
      ref={canvasRef}
      className="h-[68vh] min-h-[460px] w-full touch-none"
      role="img"
      aria-label="Force-directed graph of people and themes in your archive"
    />
  );
}
