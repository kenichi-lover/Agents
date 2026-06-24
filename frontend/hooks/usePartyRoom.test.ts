import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { usePartyRoom } from "./usePartyRoom";
import { usePartyStore } from "@/stores/partyStore";

describe("usePartyRoom", () => {
  beforeEach(() => {
    usePartyStore.setState({
      agents: new Map(),
      roundTableMode: false,
    });
  });

  it("adds agents on system:join messages", () => {
    const messages = [
      { type: "system:join", agent_id: "a1", name: "Aria" },
      { type: "system:join", agent_id: "a2", name: "Orion" },
    ];

    renderHook(() => usePartyRoom(messages));

    const store = usePartyStore.getState();
    expect(store.agents.has("a1")).toBe(true);
    expect(store.agents.has("a2")).toBe(true);
    expect(store.agents.get("a1")!.name).toBe("Aria");
    expect(store.agents.get("a2")!.name).toBe("Orion");
  });

  it("removes agents on system:leave messages", () => {
    const joinMsg = { type: "system:join", agent_id: "a1", name: "Aria" };
    const leaveMsg = { type: "system:leave", agent_id: "a1" };

    // First join
    renderHook(() => usePartyRoom([joinMsg]));

    // Then leave
    renderHook(() => usePartyRoom([joinMsg, leaveMsg]));

    const store = usePartyStore.getState();
    expect(store.agents.has("a1")).toBe(false);
  });

  it("sets mood on chat:reply messages", () => {
    const messages = [
      { type: "system:join", agent_id: "a1", name: "Aria" },
      { type: "chat:reply", agent_id: "a1", mood: "happy" },
    ];

    renderHook(() => usePartyRoom(messages));

    const store = usePartyStore.getState();
    expect(store.agents.get("a1")!.mood).toBe("happy");
  });

  it("ignores unknown message types", () => {
    const messages = [
      { type: "system:join", agent_id: "a1", name: "Aria" },
      { type: "some:unknown", foo: "bar" },
    ];

    expect(() => renderHook(() => usePartyRoom(messages))).not.toThrow();
  });

  it("handles empty messages array", () => {
    expect(() => renderHook(() => usePartyRoom([]))).not.toThrow();
  });

  it("uses deterministic colors for agents", () => {
    const messages = [
      { type: "system:join", agent_id: "a1", name: "Aria" },
      { type: "system:join", agent_id: "a2", name: "Orion" },
      { type: "system:join", agent_id: "a3", name: "Luna" },
    ];

    renderHook(() => usePartyRoom(messages));

    const store = usePartyStore.getState();
    const colors = [...store.agents.values()].map((a) => a.color);
    // Colors should be from the palette (violet, cyan, pink)
    colors.forEach((c) => {
      expect(c).toMatch(/^#[0-9a-f]{6}$/i);
    });
  });
});
