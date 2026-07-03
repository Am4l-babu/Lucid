"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Shell, PageHeader, Reveal, GhostButton } from "../ui";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Todo = {
  id: number;
  text: string;
  done: boolean;
  created: string;
  remind_at: string | null;
  notify_via: string[];
  reminded: boolean;
};

const CHANNELS = [
  { key: "telegram", label: "Telegram" },
  { key: "whatsapp", label: "WhatsApp" },
  { key: "email", label: "Email" },
  { key: "browser", label: "Browser" },
] as const;

async function jsonOrThrow(r: Response) {
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.detail ?? `HTTP ${r.status}`);
  return d;
}

function fmtReminder(iso: string) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;
  return d.toLocaleString(undefined, {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Fire browser notifications for due "browser"-channel reminders; the server
// can't push to a tab, so the page checks while it's open.
function useBrowserReminders(items: Todo[]) {
  useEffect(() => {
    const due = items.filter(
      (t) =>
        !t.done &&
        t.remind_at &&
        t.notify_via.includes("browser") &&
        new Date(t.remind_at).getTime() <= Date.now(),
    );
    if (!due.length || typeof Notification === "undefined") return;
    if (Notification.permission !== "granted") return;
    const shown: number[] = JSON.parse(localStorage.getItem("lucid-notified") ?? "[]");
    const fresh = due.filter((t) => !shown.includes(t.id));
    for (const t of fresh) new Notification("⏰ Lucid reminder", { body: t.text });
    if (fresh.length)
      localStorage.setItem(
        "lucid-notified",
        JSON.stringify([...shown, ...fresh.map((t) => t.id)].slice(-100)),
      );
  }, [items]);
}

export default function TodosPage() {
  const [items, setItems] = useState<Todo[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // add form
  const [text, setText] = useState("");
  const [remindAt, setRemindAt] = useState("");
  const [channels, setChannels] = useState<string[]>(["telegram"]);
  const [showReminder, setShowReminder] = useState(false);

  // inline edit
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editText, setEditText] = useState("");

  const refresh = useCallback(() => {
    fetch(`${API}/todos`, { signal: AbortSignal.timeout(5000) })
      .then((r) => r.json())
      .then((d) => {
        setItems(d.items ?? []);
        setLoaded(true);
        setError(null);
      })
      .catch(() => setError("Backend unreachable — is it running?"));
  }, []);

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 30_000);
    return () => clearInterval(t);
  }, [refresh]);

  useBrowserReminders(items);

  async function act(fn: () => Promise<unknown>) {
    try {
      await fn();
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    }
    refresh();
  }

  const add = () =>
    act(async () => {
      if (!text.trim()) return;
      if (channels.includes("browser") && typeof Notification !== "undefined")
        Notification.requestPermission();
      await jsonOrThrow(
        await fetch(`${API}/todos`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text,
            remind_at: showReminder && remindAt ? remindAt : null,
            notify_via: showReminder && remindAt ? channels : [],
          }),
        }),
      );
      setText("");
      setRemindAt("");
      setShowReminder(false);
    });

  const toggle = (t: Todo) =>
    act(async () => {
      await jsonOrThrow(
        await fetch(`${API}/todos/${t.id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ done: !t.done }),
        }),
      );
    });

  const saveEdit = (t: Todo) =>
    act(async () => {
      if (editText.trim() && editText !== t.text)
        await jsonOrThrow(
          await fetch(`${API}/todos/${t.id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: editText }),
          }),
        );
      setEditingId(null);
    });

  const remove = (t: Todo) =>
    act(async () => {
      await jsonOrThrow(await fetch(`${API}/todos/${t.id}`, { method: "DELETE" }));
    });

  const clearReminder = (t: Todo) =>
    act(async () => {
      await jsonOrThrow(
        await fetch(`${API}/todos/${t.id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ clear_reminder: true }),
        }),
      );
    });

  const open = items.filter((t) => !t.done);
  const closed = items.filter((t) => t.done);

  return (
    <Shell>
      <PageHeader
        kicker="Tasks"
        title="Todos"
        lead="One list everywhere — edit it here or chat with your Telegram bot (/todo, /add, /done). Reminders arrive on the channels you pick."
      />

      <Reveal className="flex flex-col gap-8">
        {/* Add */}
        <div className="card flex flex-col gap-3 p-5 sm:p-6">
          <div className="flex gap-2">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && add()}
              placeholder="Add a todo — press Enter"
              className="h-11 w-full rounded-lg border border-line-2 bg-surface-2 px-4 text-[0.9rem] text-ink placeholder:text-faint focus:border-faint focus:outline-none"
            />
            <GhostButton onClick={add} disabled={!text.trim()}>
              Add
            </GhostButton>
          </div>

          <button
            onClick={() => setShowReminder((s) => !s)}
            className="self-start font-mono text-[0.6rem] uppercase tracking-[0.18em] text-faint underline decoration-line-2 underline-offset-4 hover:text-muted"
          >
            {showReminder ? "− Remove reminder" : "+ Set a reminder"}
          </button>

          {showReminder && (
            <div className="flex flex-wrap items-center gap-3 rounded-lg border border-line bg-surface-2/50 p-3">
              <input
                type="datetime-local"
                value={remindAt}
                onChange={(e) => setRemindAt(e.target.value)}
                className="h-9 rounded-lg border border-line-2 bg-surface-2 px-3 font-mono text-[0.72rem] text-ink focus:border-faint focus:outline-none [color-scheme:dark]"
              />
              <div className="flex flex-wrap gap-1.5">
                {CHANNELS.map((c) => {
                  const on = channels.includes(c.key);
                  return (
                    <button
                      key={c.key}
                      onClick={() =>
                        setChannels((prev) =>
                          on ? prev.filter((k) => k !== c.key) : [...prev, c.key],
                        )
                      }
                      className={`rounded-full border px-3 py-1.5 font-mono text-[0.6rem] uppercase tracking-[0.15em] transition-colors ${
                        on
                          ? "border-accent/50 bg-accent/10 text-ink"
                          : "border-line-2 text-faint hover:text-muted"
                      }`}
                    >
                      {c.label}
                    </button>
                  );
                })}
              </div>
              <span className="w-full font-mono text-[0.58rem] tracking-wide text-faint">
                Telegram needs the bot connected · WhatsApp needs the bridge running ·
                Email needs Google reconnected once (send permission) · Browser fires
                while this page is open
              </span>
            </div>
          )}
        </div>

        {error && (
          <span className="font-mono text-[0.65rem] tracking-wide text-muted">✗ {error}</span>
        )}

        {/* Open items */}
        <div className="flex flex-col gap-2">
          {loaded && open.length === 0 && closed.length === 0 && !error && (
            <p className="text-[0.85rem] text-muted">
              Nothing here yet. Add one above — or send <span className="font-mono">/add buy milk</span> to your Telegram bot.
            </p>
          )}
          {open.map((t) => (
            <TodoRow
              key={t.id}
              todo={t}
              editing={editingId === t.id}
              editText={editText}
              setEditText={setEditText}
              onToggle={() => toggle(t)}
              onStartEdit={() => {
                setEditingId(t.id);
                setEditText(t.text);
              }}
              onSaveEdit={() => saveEdit(t)}
              onCancelEdit={() => setEditingId(null)}
              onDelete={() => remove(t)}
              onClearReminder={() => clearReminder(t)}
            />
          ))}
        </div>

        {/* Done items */}
        {closed.length > 0 && (
          <div className="flex flex-col gap-2">
            <span className="font-mono text-[0.6rem] uppercase tracking-[0.2em] text-faint">
              Done — {closed.length}
            </span>
            {closed.map((t) => (
              <TodoRow
                key={t.id}
                todo={t}
                editing={false}
                editText=""
                setEditText={() => {}}
                onToggle={() => toggle(t)}
                onStartEdit={() => {}}
                onSaveEdit={() => {}}
                onCancelEdit={() => {}}
                onDelete={() => remove(t)}
                onClearReminder={() => clearReminder(t)}
              />
            ))}
          </div>
        )}
      </Reveal>
    </Shell>
  );
}

function TodoRow({
  todo,
  editing,
  editText,
  setEditText,
  onToggle,
  onStartEdit,
  onSaveEdit,
  onCancelEdit,
  onDelete,
  onClearReminder,
}: {
  todo: Todo;
  editing: boolean;
  editText: string;
  setEditText: (s: string) => void;
  onToggle: () => void;
  onStartEdit: () => void;
  onSaveEdit: () => void;
  onCancelEdit: () => void;
  onDelete: () => void;
  onClearReminder: () => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (editing) inputRef.current?.focus();
  }, [editing]);

  const overdue =
    !todo.done && todo.remind_at && new Date(todo.remind_at).getTime() <= Date.now();

  return (
    <div className="card group flex items-center gap-3 px-4 py-3">
      <button
        onClick={onToggle}
        aria-label={todo.done ? "Mark as not done" : "Mark as done"}
        className={`grid h-5 w-5 shrink-0 place-items-center rounded-md border transition-colors ${
          todo.done
            ? "border-accent/60 bg-accent/20 text-accent"
            : "border-line-2 hover:border-faint"
        }`}
      >
        {todo.done && (
          <svg viewBox="0 0 12 12" className="h-3 w-3" fill="none" aria-hidden="true">
            <path d="M2 6l3 3 5-6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </button>

      {editing ? (
        <input
          ref={inputRef}
          value={editText}
          onChange={(e) => setEditText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") onSaveEdit();
            if (e.key === "Escape") onCancelEdit();
          }}
          onBlur={onSaveEdit}
          className="h-8 w-full rounded-md border border-line-2 bg-surface-2 px-2 text-[0.88rem] text-ink focus:border-faint focus:outline-none"
        />
      ) : (
        <button
          onClick={todo.done ? undefined : onStartEdit}
          className={`min-w-0 flex-1 truncate text-left text-[0.88rem] ${
            todo.done ? "text-faint line-through" : "text-ink hover:text-muted"
          }`}
          title={todo.done ? undefined : "Click to edit"}
        >
          {todo.text}
        </button>
      )}

      {todo.remind_at && !todo.done && (
        <button
          onClick={onClearReminder}
          title="Click to remove this reminder"
          className={`shrink-0 rounded-full border px-2.5 py-1 font-mono text-[0.58rem] tracking-wide ${
            overdue
              ? "border-accent/50 text-accent"
              : "border-line-2 text-faint hover:text-muted"
          }`}
        >
          ⏰ {fmtReminder(todo.remind_at)}
          {todo.notify_via.length > 0 && ` · ${todo.notify_via.join(", ")}`}
        </button>
      )}

      <button
        onClick={onDelete}
        aria-label="Delete todo"
        className="shrink-0 rounded-md px-1.5 text-faint opacity-0 transition-opacity hover:text-muted group-hover:opacity-100"
      >
        ✕
      </button>
    </div>
  );
}
