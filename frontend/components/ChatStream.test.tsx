import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { ChatStream } from "./ChatStream";

/* ── helpers ──────────────────────────────────────────────── */

function renderChat(props: Partial<React.ComponentProps<typeof ChatStream>> = {}) {
  const onSend = vi.fn();
  render(
    <div className="flex flex-col h-64">
      <ChatStream
        messages={[]}
        onSend={onSend}
        sendStatus="idle"
        {...props}
      />
    </div>,
  );
  return { onSend };
}

/* ── empty state ──────────────────────────────────────────── */

describe("empty state", () => {
  it("shows placeholder when no messages", () => {
    renderChat({});
    expect(screen.getByText(/No messages yet/i)).toBeInTheDocument();
  });
});

/* ── message rendering ────────────────────────────────────── */

describe("message rendering", () => {
  it("renders system:join message", () => {
    renderChat({ messages: [{ type: "system:join", name: "Aria" }] });
    expect(screen.getByText("joined — Aria")).toBeInTheDocument();
  });

  it("renders system:leave message", () => {
    renderChat({ messages: [{ type: "system:leave", name: "Orion" }] });
    expect(screen.getByText("left — Orion")).toBeInTheDocument();
  });

  it("renders user message", () => {
    renderChat({ messages: [{ type: "chat:message", content: "Hello!", is_user: true }] });
    expect(screen.getByText("Hello!")).toBeInTheDocument();
  });

  it("renders agent reply", () => {
    renderChat({ messages: [{ type: "chat:reply", content: "Hi there!", agent_id: "agent-1", message_id: "m1" }] });
    expect(screen.getByText("Hi there!")).toBeInTheDocument();
  });

  it("renders agent message", () => {
    renderChat({ messages: [{ type: "chat:message", content: "Agent speaks", agent_id: "agent-2" }] });
    expect(screen.getByText("Agent speaks")).toBeInTheDocument();
  });

  it("filters thinking when reply exists for same message_id", () => {
    renderChat({
      messages: [
        { type: "chat:thinking", message_id: "m1" },
        { type: "chat:reply", content: "Replaced!", message_id: "m1" },
      ],
    });
    expect(screen.getByText("Replaced!")).toBeInTheDocument();
    // thinking bubble dots should not appear
    expect(document.querySelectorAll(".animate-bounce").length).toBe(0);
  });

  it("shows thinking bubble", () => {
    renderChat({ messages: [{ type: "chat:thinking", agent_id: "agent-1" }] });
    // thinking shows 3 bounce dots
    expect(document.querySelectorAll(".animate-bounce").length).toBe(3);
  });

  it("renders fallback for unknown message type", () => {
    renderChat({ messages: [{ type: "custom:type", content: "unknown" }] });
    expect(screen.getByText("unknown")).toBeInTheDocument();
  });
});

/* ── input & sending ──────────────────────────────────────── */

describe("input & sending", () => {
  it("calls onSend with trimmed input on button click", () => {
    const { onSend } = renderChat({});
    const input = screen.getByPlaceholderText(/Type/i);
    const button = screen.getByRole("button", { name: /Send/i });

    fireEvent.change(input, { target: { value: "  hello  " } });
    fireEvent.click(button);

    expect(onSend).toHaveBeenCalledWith("hello");
  });

  it("does not send when input is empty", () => {
    const { onSend } = renderChat({});
    const button = screen.getByRole("button", { name: /Send/i });
    fireEvent.click(button);
    expect(onSend).not.toHaveBeenCalled();
  });

  it("disables send button when input is empty", () => {
    renderChat({});
    const button = screen.getByRole("button", { name: /Send/i });
    expect(button).toBeDisabled();
  });

  it("sends on Enter key", () => {
    const { onSend } = renderChat({});
    const input = screen.getByPlaceholderText(/Type/i);
    fireEvent.change(input, { target: { value: "enter msg" } });
    fireEvent.keyDown(input, { key: "Enter" });
    expect(onSend).toHaveBeenCalledWith("enter msg");
  });
});

/* ── status banner ────────────────────────────────────────── */

describe("send status banner", () => {
  it("shows sending banner", () => {
    renderChat({ sendStatus: "sending" });
    expect(screen.getByText(/发送中/i)).toBeInTheDocument();
  });

  it("shows error banner", () => {
    renderChat({ sendStatus: "error" });
    expect(screen.getByText(/连接已断开/i)).toBeInTheDocument();
  });

  it("hides banner when idle", () => {
    renderChat({ sendStatus: "idle" });
    expect(screen.queryByText(/发送中/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/连接已断开/i)).not.toBeInTheDocument();
  });
});
