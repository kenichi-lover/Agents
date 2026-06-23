# Party Page Components Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 4 missing components (ChatStream, AgentPanel, PresenceBar, RoundTable), fix the party page layout, and redirect the home page to /login.

**Architecture:** Four small focused components wired into the existing party/[partyId]/page.tsx three-column layout. Mock data for agents and participants; real WebSocket integration via the existing useWebSocket hook.

**Tech Stack:** React 19, Next.js 15 App Router, TypeScript 5, Tailwind CSS 4, Framer Motion 11 (for thinking animation), VANTA (already on login page).

## Global Constraints

- All components ≤ 200 lines each (CLAUDE.md §3.2)
- `"use client"` only on components that use hooks/state
- Custom hooks must start with `use`
- All types defined inline or in shared types (no `any` unless unavoidable)
- UUID primary keys for entities (CLAUDE.md §3.3)
- Snake case for Python, camelCase for TS, PascalCase for components
- Dark tech style: slate-900 background, violet-600 primary, emerald-400 online indicator, cyan accents

---

### Task 1: Redirect Home Page

**Files:**
- Modify: `frontend/app/page.tsx`

**Interfaces:**
- Consumes: Next.js `redirect` from `next/navigation`
- Produces: Home page redirects to `/login`

- [ ] **Step 1: Replace page.tsx with redirect**

Remove the entire Next.js scaffolding content. Replace with a client component that redirects to `/login`:

```tsx
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();
  useEffect(() => { router.replace("/login"); }, [router]);
  return null;
}
```

- [ ] **Step 2: Verify build**

Run: `cd frontend && npx tsc --noEmit`

Expected: No TypeScript errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/app/page.tsx
git commit -m "feat: redirect home page to /login"
```

---

### Task 2: PresenceBar Component

**Files:**
- Create: `frontend/components/PresenceBar.tsx`

**Interfaces:**
- Consumes: `isConnected: boolean`, `partyId: string`
- Produces: Top bar showing connection status (green/red dot + text) and participant count

- [ ] **Step 1: Create PresenceBar component**

```tsx
"use client";

interface PresenceBarProps {
  isConnected: boolean;
  partyId: string;
}

export function PresenceBar({ isConnected, partyId }: PresenceBarProps) {
  return (
    <div className="flex items-center justify-between px-4 py-2 bg-slate-800 border-b border-slate-700">
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-slate-300">
          Party #{partyId.slice(0, 8)}
        </span>
        <span className="text-xs text-slate-500">|</span>
        <div className="flex items-center gap-1.5">
          <span
            className={`w-2 h-2 rounded-full ${
              isConnected ? "bg-emerald-400" : "bg-red-400"
            }`}
          />
          <span className="text-xs text-slate-400">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>
      <div className="flex items-center gap-2 text-xs text-slate-400">
        <span className="hidden sm:inline">2 agents · 1 human</span>
        <span className="sm:hidden">3 online</span>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/components/PresenceBar.tsx
git commit -m "feat: add PresenceBar component"
```

---

### Task 3: AgentPanel Component

**Files:**
- Create: `frontend/components/AgentPanel.tsx`

**Interfaces:**
- Consumes: `onPromptAgent(agentId: string, prompt: string): void`
- Produces: Left sidebar listing agents with avatar, name, online dot, and prompt input per agent

- [ ] **Step 1: Create AgentPanel component**

```tsx
"use client";

interface Agent {
  id: string;
  name: string;
  color: string;
  online: boolean;
}

const MOCK_AGENTS: Agent[] = [
  { id: "agent-1", name: "Aria", color: "bg-violet-500", online: true },
  { id: "agent-2", name: "Orion", color: "bg-cyan-500", online: true },
  { id: "agent-3", name: "Luna", color: "bg-pink-500", online: false },
];

interface AgentPanelProps {
  onPromptAgent: (agentId: string, prompt: string) => void;
}

export function AgentPanel({ onPromptAgent }: AgentPanelProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [promptText, setPromptText] = useState("");

  const handlePrompt = () => {
    if (!promptText.trim() || !expandedId) return;
    onPromptAgent(expandedId, promptText.trim());
    setPromptText("");
  };

  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Agents
      </h3>

      <div className="space-y-1 flex-1 overflow-y-auto">
        {MOCK_AGENTS.map((agent) => (
          <div key={agent.id}>
            {/* Agent row */}
            <button
              onClick={() => setExpandedId(expandedId === agent.id ? null : agent.id)}
              className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm transition hover:bg-slate-800 ${
                expandedId === agent.id ? "bg-slate-800" : ""
              }`}
            >
              <span className={`w-6 h-6 rounded-full ${agent.color} flex items-center justify-center text-xs font-bold text-white`}>
                {agent.name[0]}
              </span>
              <span className="flex-1 text-left text-slate-200">{agent.name}</span>
              <span
                className={`w-2 h-2 rounded-full ${
                  agent.online ? "bg-emerald-400" : "bg-slate-600"
                }`}
              />
            </button>

            {/* Expanded prompt input */}
            {expandedId === agent.id && (
              <div className="mx-2 mt-1 pb-2">
                <div className="flex gap-1">
                  <input
                    type="text"
                    value={promptText}
                    onChange={(e) => setPromptText(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handlePrompt()}
                    placeholder={`Message ${agent.name}...`}
                    className="flex-1 px-2 py-1 text-xs rounded bg-slate-800 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500"
                  />
                  <button
                    onClick={handlePrompt}
                    disabled={!promptText.trim()}
                    className="px-2 py-1 text-xs rounded bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white transition"
                  >
                    Send
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

Wait — this uses `useState` but is missing the import. Let me fix:

```tsx
"use client";

import { useState } from "react";

interface Agent {
  id: string;
  name: string;
  color: string;
  online: boolean;
}

const MOCK_AGENTS: Agent[] = [
  { id: "agent-1", name: "Aria", color: "bg-violet-500", online: true },
  { id: "agent-2", name: "Orion", color: "bg-cyan-500", online: true },
  { id: "agent-3", name: "Luna", color: "bg-pink-500", online: false },
];

interface AgentPanelProps {
  onPromptAgent: (agentId: string, prompt: string) => void;
}

export function AgentPanel({ onPromptAgent }: AgentPanelProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [promptText, setPromptText] = useState("");

  const handlePrompt = () => {
    if (!promptText.trim() || !expandedId) return;
    onPromptAgent(expandedId, promptText.trim());
    setPromptText("");
  };

  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Agents
      </h3>

      <div className="space-y-1 flex-1 overflow-y-auto">
        {MOCK_AGENTS.map((agent) => (
          <div key={agent.id}>
            <button
              onClick={() => setExpandedId(expandedId === agent.id ? null : agent.id)}
              className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm transition hover:bg-slate-800 ${
                expandedId === agent.id ? "bg-slate-800" : ""
              }`}
            >
              <span className={`w-6 h-6 rounded-full ${agent.color} flex items-center justify-center text-xs font-bold text-white`}>
                {agent.name[0]}
              </span>
              <span className="flex-1 text-left text-slate-200">{agent.name}</span>
              <span
                className={`w-2 h-2 rounded-full ${
                  agent.online ? "bg-emerald-400" : "bg-slate-600"
                }`}
              />
            </button>

            {expandedId === agent.id && (
              <div className="mx-2 mt-1 pb-2">
                <div className="flex gap-1">
                  <input
                    type="text"
                    value={promptText}
                    onChange={(e) => setPromptText(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handlePrompt()}
                    placeholder={`Message ${agent.name}...`}
                    className="flex-1 px-2 py-1 text-xs rounded bg-slate-800 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500"
                  />
                  <button
                    onClick={handlePrompt}
                    disabled={!promptText.trim()}
                    className="px-2 py-1 text-xs rounded bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white transition"
                  >
                    Send
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/components/AgentPanel.tsx
git commit -m "feat: add AgentPanel component"
```

---

### Task 4: ChatStream Component

**Files:**
- Create: `frontend/components/ChatStream.tsx`

**Interfaces:**
- Consumes: `messages: WebSocketMessage[]`, `onSend(content: string): void`
- Produces: Scrollable message area with bubbles + input bar

**Message type conventions (from `useWebSocket` and `lib/websocket.ts`):**
- `chat:message` — regular message (has `type`, `content`, `agent_id` or `user_id`)
- `chat:thinking` — agent is thinking (has `type`, `agent_id`, `message_id`)
- `chat:reply` — agent finished thinking, replaces the thinking message (has `type`, `message_id`, `content`)
- `system:join` / `system:leave` — user/agent joined/left (has `type`, `name`)

- [ ] **Step 1: Create ChatStream component**

```tsx
"use client";

import { useState, useRef, useEffect } from "react";

interface ChatMessage {
  type: string;
  content?: string;
  agent_id?: string;
  user_id?: string;
  name?: string;
  message_id?: string;
  timestamp?: string;
}

interface ChatStreamProps {
  messages: ChatMessage[];
  onSend: (content: string) => void;
}

const AGENT_AVATARS: Record<string, { name: string; color: string }> = {
  "agent-1": { name: "Aria", color: "bg-violet-500" },
  "agent-2": { name: "Orion", color: "bg-cyan-500" },
  "agent-3": { name: "Luna", color: "bg-pink-500" },
};

export function ChatStream({ messages, onSend }: ChatStreamProps) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setInput("");
  };

  // Group messages: thinking messages are replaced by replies
  // We track message_id -> thinking status
  const thinkingMap = new Map<string, boolean>();
  const replyMap = new Map<string, string>(); // message_id -> reply content

  for (const msg of messages) {
    if (msg.type === "chat:thinking" && msg.message_id) {
      thinkingMap.set(msg.message_id, true);
    }
    if (msg.type === "chat:reply" && msg.message_id && msg.content) {
      replyMap.set(msg.message_id, msg.content);
    }
  }

  const hasSystem = (type: string) => type.startsWith("system:");
  const hasChat = (type: string) => type === "chat:message" || type === "chat:thinking" || type === "chat:reply";

  // Filter: if a thinking message's id has a reply, skip the thinking
  const visibleMessages = messages.filter((msg) => {
    if (msg.type === "chat:thinking" && replyMap.has(msg.message_id ?? "")) {
      return false;
    }
    return true;
  });

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div
        ref={scrollContainerRef}
        className="flex-1 overflow-y-auto px-4 py-3 space-y-3"
      >
        {visibleMessages.length === 0 && (
          <div className="flex items-center justify-center h-full text-slate-500 text-sm">
            No messages yet — start the conversation!
          </div>
        )}

        {visibleMessages.map((msg, i) => {
          // System messages
          if (hasSystem(msg.type)) {
            return (
              <div key={i} className="flex items-center justify-center text-xs text-slate-500 py-1">
                <span className="bg-slate-800 px-3 py-1 rounded-full">
                  {msg.type === "system:join" ? "joined" : msg.type === "system:leave" ? "left" : msg.type}
                  {msg.name ? ` — ${msg.name}` : ""}
                </span>
              </div>
            );
          }

          // Thinking bubble
          if (msg.type === "chat:thinking") {
            return (
              <div key={i} className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-violet-500 flex-shrink-0 flex items-center justify-center text-xs font-bold text-white">
                  ?
                </div>
                <div className="bg-slate-800 rounded-2xl rounded-tl-sm px-3 py-2 max-w-sm">
                  <div className="flex gap-1">
                    <span className="animate-bounce text-slate-400">.</span>
                    <span className="animate-bounce text-slate-400" style={{ animationDelay: "0.15s" }}>.</span>
                    <span className="animate-bounce text-slate-400" style={{ animationDelay: "0.3s" }}>.</span>
                  </div>
                </div>
              </div>
            );
          }

          // Reply (replaces thinking)
          if (msg.type === "chat:reply") {
            const agent = AGENT_AVATARS[msg.agent_id ?? ""] ?? { name: "?", color: "bg-slate-500" };
            return (
              <div key={i} className="flex items-start gap-2">
                <div className={`w-6 h-6 rounded-full ${agent.color} flex-shrink-0 flex items-center justify-center text-xs font-bold text-white`}>
                  {agent.name[0]}
                </div>
                <div className="bg-slate-700 rounded-2xl rounded-tl-sm px-3 py-2 max-w-md text-sm text-slate-200">
                  {msg.content}
                </div>
              </div>
            );
          }

          // Regular chat message
          const isUser = !msg.agent_id;
          const agent = AGENT_AVATARS[msg.agent_id ?? ""];
          if (agent) {
            return (
              <div key={i} className="flex items-start gap-2">
                <div className={`w-6 h-6 rounded-full ${agent.color} flex-shrink-0 flex items-center justify-center text-xs font-bold text-white`}>
                  {agent.name[0]}
                </div>
                <div className="bg-slate-700 rounded-2xl rounded-tl-sm px-3 py-2 max-w-md text-sm text-slate-200">
                  {msg.content}
                </div>
              </div>
            );
          }

          // User message
          return (
            <div key={i} className="flex items-start gap-2 justify-end">
              <div className="bg-violet-600 rounded-2xl rounded-tr-sm px-3 py-2 max-w-md text-sm text-white">
                {msg.content}
              </div>
            </div>
          );
        })}

        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="border-t border-slate-700 px-4 py-3">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type a message..."
            className="flex-1 px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500 text-sm"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim()}
            className="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

Let me count lines — this is about 140 lines. Under 200. Good.

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/components/ChatStream.tsx
git commit -m "feat: add ChatStream component"
```

---

### Task 5: RoundTable Component (Placeholder)

**Files:**
- Create: `frontend/components/RoundTable.tsx`

**Interfaces:**
- Consumes: `partyId: string`
- Produces: Right sidebar with "Coming soon" placeholder

- [ ] **Step 1: Create RoundTable placeholder**

```tsx
"use client";

interface RoundTableProps {
  partyId: string;
}

export function RoundTable({ partyId }: RoundTableProps) {
  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Round Table
      </h3>
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="text-3xl mb-2">🍽️</div>
          <p className="text-sm text-slate-500">Coming soon</p>
          <p className="text-xs text-slate-600 mt-1">
            Group conversations & threads
          </p>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/components/RoundTable.tsx
git commit -m "feat: add RoundTable placeholder component"
```

---

### Task 6: Wire Components into Party Page

**Files:**
- Modify: `frontend/app/party/[partyId]/page.tsx`

**Interfaces:**
- Consumes: `PresenceBar`, `AgentPanel`, `ChatStream`, `RoundTable`
- Produces: Fully wired party room page

- [ ] **Step 1: Update party/[partyId]/page.tsx**

```tsx
"use client";

import { useWebSocket } from "@/hooks/useWebSocket";
import { ChatStream } from "@/components/ChatStream";
import { AgentPanel } from "@/components/AgentPanel";
import { PresenceBar } from "@/components/PresenceBar";
import { RoundTable } from "@/components/RoundTable";

export default function PartyRoom({ params }: { params: Promise<{ partyId: string }> }) {
  const [resolved] = useState(() => params);
  const partyId = resolved?.partyId ?? "unknown";
  const token = ""; // TODO: from auth context / localStorage
  const { isConnected, messages, sendMessage } = useWebSocket(partyId, token);

  const handleSendMessage = (content: string) => {
    sendMessage({
      type: "chat:message",
      content,
      timestamp: new Date().toISOString(),
    });
  };

  const handlePromptAgent = (agentId: string, prompt: string) => {
    sendMessage({
      type: "user:prompt",
      target_agent: agentId,
      content: prompt,
    });
  };

  return (
    <div className="h-screen flex flex-col bg-slate-900 text-white">
      <PresenceBar isConnected={isConnected} partyId={partyId} />

      <div className="flex-1 flex overflow-hidden">
        <aside className="w-64 border-r border-slate-700 p-4">
          <AgentPanel onPromptAgent={handlePromptAgent} />
        </aside>

        <main className="flex-1 flex flex-col">
          <ChatStream messages={messages} onSend={handleSendMessage} />
        </main>

        <aside className="w-80 border-l border-slate-700 p-4">
          <RoundTable partyId={partyId} />
        </aside>
      </div>
    </div>
  );
}
```

Wait — `useState(() => params)` won't work correctly. In Next.js 15+, `params` is a Promise. The correct pattern:

```tsx
"use client";

import { useEffect, useState } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { ChatStream } from "@/components/ChatStream";
import { AgentPanel } from "@/components/AgentPanel";
import { PresenceBar } from "@/components/PresenceBar";
import { RoundTable } from "@/components/RoundTable";

export default function PartyRoom({ params }: { params: Promise<{ partyId: string }> }) {
  const [partyId, setPartyId] = useState("");

  useEffect(() => {
    params.then((p) => setPartyId(p.partyId));
  }, [params]);

  const token = ""; // TODO: from auth context / localStorage
  const { isConnected, messages, sendMessage } = useWebSocket(partyId, token);

  const handleSendMessage = (content: string) => {
    sendMessage({
      type: "chat:message",
      content,
      timestamp: new Date().toISOString(),
    });
  };

  const handlePromptAgent = (agentId: string, prompt: string) => {
    sendMessage({
      type: "user:prompt",
      target_agent: agentId,
      content: prompt,
    });
  };

  if (!partyId) return null;

  return (
    <div className="h-screen flex flex-col bg-slate-900 text-white">
      <PresenceBar isConnected={isConnected} partyId={partyId} />

      <div className="flex-1 flex overflow-hidden">
        <aside className="w-64 border-r border-slate-700 p-4">
          <AgentPanel onPromptAgent={handlePromptAgent} />
        </aside>

        <main className="flex-1 flex flex-col">
          <ChatStream messages={messages} onSend={handleSendMessage} />
        </main>

        <aside className="w-80 border-l border-slate-700 p-4">
          <RoundTable partyId={partyId} />
        </aside>
      </div>
    </div>
  );
}
```

Actually — simpler and more idiomatic in Next.js 15: use `use` from React to unwrap the Promise:

```tsx
"use client";

import { use } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { ChatStream } from "@/components/ChatStream";
import { AgentPanel } from "@/components/AgentPanel";
import { PresenceBar } from "@/components/PresenceBar";
import { RoundTable } from "@/components/RoundTable";

export default function PartyRoom({ params }: { params: Promise<{ partyId: string }> }) {
  const { partyId } = use(params);
  const token = ""; // TODO: from auth context / localStorage
  const { isConnected, messages, sendMessage } = useWebSocket(partyId, token);

  const handleSendMessage = (content: string) => {
    sendMessage({
      type: "chat:message",
      content,
      timestamp: new Date().toISOString(),
    });
  };

  const handlePromptAgent = (agentId: string, prompt: string) => {
    sendMessage({
      type: "user:prompt",
      target_agent: agentId,
      content: prompt,
    });
  };

  return (
    <div className="h-screen flex flex-col bg-slate-900 text-white">
      <PresenceBar isConnected={isConnected} partyId={partyId} />

      <div className="flex-1 flex overflow-hidden">
        <aside className="w-64 border-r border-slate-700 p-4">
          <AgentPanel onPromptAgent={handlePromptAgent} />
        </aside>

        <main className="flex-1 flex flex-col">
          <ChatStream messages={messages} onSend={handleSendMessage} />
        </main>

        <aside className="w-80 border-l border-slate-700 p-4">
          <RoundTable partyId={partyId} />
        </aside>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript compiles**

Run: `cd frontend && npx tsc --noEmit`

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/app/party/\[partyId\]/page.tsx
git commit -m "feat: wire party page with all components, fix params type"
```

---

## Self-Review

**1. Spec coverage:**
- Redirect home page → Task 1 ✓
- PresenceBar (connection status + participant count) → Task 2 ✓
- AgentPanel (avatar + name + online dot + prompt input) → Task 3 ✓
- ChatStream (bubbles, thinking animation, reply replace) → Task 4 ✓
- RoundTable placeholder → Task 5 ✓
- Wire components into party page + fix params → Task 6 ✓
- Dark tech style (slate-900, violet-600, emerald-400) → Tasks 2-5 ✓

**2. Placeholder scan:**
- No "TBD", "TODO" (except `// TODO: from auth context` which is intentional and noted)
- All code is complete with actual implementations
- All component props are fully specified

**3. Type consistency:**
- `useWebSocket` returns `{ isConnected, messages, sendMessage }` — used consistently across Tasks 4, 6
- `sendMessage` accepts `WebSocketMessage` (`{ type: string, [key: string]: any }`) — all calls pass valid objects
- `ChatStream.onSend` takes `(content: string) => void` — matches Task 4 and Task 6
- `AgentPanel.onPromptAgent` takes `(agentId: string, prompt: string) => void` — matches Task 3 and Task 6
- All components use `"use client"` — consistent

**4. Scope check:**
- 6 tasks, each produces independently testable deliverables
- No cross-task dependencies beyond file creation order
- Each task has its own commit

---

Plan complete and saved to `docs/superpowers/plans/2026-06-23-party-page-components.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
