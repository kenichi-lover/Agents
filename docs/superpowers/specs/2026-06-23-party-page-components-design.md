# Party Page Components — Design Spec

> Date: 2026-06-23
> Status: Approved

## Summary

Build four missing UI components for the Agent Party room page, fix routing on the home page, and wire them into the existing `party/[partyId]/page.tsx` layout.

## Decisions

| # | Topic | Choice |
|---|-------|--------|
| 1 | Component granularity | Split into 4 independent files |
| 2 | AgentPanel content | Avatar + name + online dot + prompt input |
| 3 | ChatStream messages | Thinking bubble → smooth replace with formal message |
| 4 | Home page | Redirect to `/login` |
| 5 | Visual style | Dark tech (slate-900 + purple/cyan accents) |

## Files to Create / Modify

### Modified

1. **`app/page.tsx`** — Replace Next.js scaffolding with redirect to `/login`.
2. **`app/party/[partyId]/page.tsx`** — `await params`, inject mock token for now, fix type signature.

### Created

3. **`components/ChatStream.tsx`** — Scrollable message list + input bar.
   - Renders `chat:message` as bubbles (user right/blue, agent left/with avatar).
   - Renders `chat:thinking` as gray spinner bubble; on `chat:reply` (new type), replaces thinking in-place.
   - Renders `system:*` as small gray divider text.
   - Input bar: text field + send button, calls `onSend`.

4. **`components/AgentPanel.tsx`** — Left sidebar (w-64).
   - Lists agents from mock data: avatar (initials), name, green online dot.
   - Each row has a "Prompt" button that opens a small input below the list.
   - Prompt button calls `onPromptAgent(agentId, text)`.

5. **`components/PresenceBar.tsx`** — Top bar.
   - Shows connection status indicator (green/red dot + text).
   - Shows party name/ID.
   - Lists connected participants (mock data + WebSocket join events).

6. **`components/RoundTable.tsx`** — Right sidebar (w-80).
   - Placeholder for now: header + "Coming soon" message.
   - Reserved for future grouping/conversation thread visualization.

## Data Flow

```
User types in ChatStream input
    │
    ▼
handleSendMessage({ type: "chat:message", content, ... })
    │
    ▼
useWebSocket.sendMessage(JSON.stringify(msg))
    │
    ▼
WebSocket sends to backend → broadcasts to room
    │
    ▼
All clients receive via onmessage → appended to messages array
    │
    ▼
ChatStream re-renders with new bubble
```

## Error Handling

- WebSocket disconnected: PresenceBar shows red indicator; ChatStream input disabled.
- Empty messages: ChatStream shows "No messages yet — start the conversation!" placeholder.
- No agents loaded: AgentPanel shows "Loading agents..." skeleton (will be replaced by API call).

## Visual Design

- Background: `bg-slate-900`
- Chat bubbles: user `bg-violet-600` right-aligned, agent `bg-slate-700` left-aligned
- Thinking: `bg-slate-800` with pulsing dots animation
- Online indicator: `bg-emerald-400` green dot
- Accent colors: violet (primary), cyan (secondary highlights)
- Font: Geist Sans (already in layout)
