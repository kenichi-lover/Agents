import { usePartyStore, type AgentEntry } from "./partyStore";

/* ── helper to reset store ────────────────────────────────── */

function resetStore() {
  usePartyStore.setState({
    agents: new Map(),
    roundTableMode: false,
  });
}

function getStore() {
  return usePartyStore.getState();
}

describe("partyStore", () => {
  beforeEach(resetStore);

  /* ── addAgent ──────────────────────────────────────────── */

  it("adds a new agent with deterministic position", () => {
    getStore().addAgent("agent-1", "Aria", "bg-violet-500");
    const agent = getStore().agents.get("agent-1");
    expect(agent).toBeDefined();
    expect(agent!.name).toBe("Aria");
    expect(agent!.color).toBe("bg-violet-500");
    expect(agent!.mood).toBe("neutral");
    expect(agent!.position).toEqual(agent!.targetPosition);
  });

  it("is idempotent — adding twice does not duplicate", () => {
    getStore().addAgent("a1", "A", "bg-red-500");
    getStore().addAgent("a1", "A2", "bg-blue-500");
    expect(getStore().agents.size).toBe(1);
    expect(getStore().agents.get("a1")!.name).toBe("A");
  });

  it("different agents get different positions", () => {
    getStore().addAgent("x", "X", "bg-x");
    getStore().addAgent("y", "Y", "bg-y");
    const posX = getStore().agents.get("x")!.position;
    const posY = getStore().agents.get("y")!.position;
    expect(posX).not.toEqual(posY);
  });

  /* ── removeAgent ───────────────────────────────────────── */

  it("removes an existing agent", () => {
    getStore().addAgent("a1", "A", "bg-a");
    getStore().removeAgent("a1");
    expect(getStore().agents.has("a1")).toBe(false);
  });

  it("silently ignores removing non-existent agent", () => {
    expect(() => getStore().removeAgent("nope")).not.toThrow();
    expect(getStore().agents.size).toBe(0);
  });

  /* ── setAgentPosition ──────────────────────────────────── */

  it("updates targetPosition of existing agent", () => {
    getStore().addAgent("a1", "A", "bg-a");
    getStore().setAgentPosition("a1", [1, 0, 2]);
    const agent = getStore().agents.get("a1");
    expect(agent!.targetPosition).toEqual([1, 0, 2]);
  });

  it("silently ignores non-existent agent", () => {
    expect(() => getStore().setAgentPosition("nope", [0, 0, 0])).not.toThrow();
  });

  /* ── setMood ───────────────────────────────────────────── */

  it("updates agent mood", () => {
    getStore().addAgent("a1", "A", "bg-a");
    getStore().setMood("a1", "happy");
    expect(getStore().agents.get("a1")!.mood).toBe("happy");
  });

  /* ── round table mode ──────────────────────────────────── */

  it("toggles roundTableMode", () => {
    expect(getStore().roundTableMode).toBe(false);
    getStore().setRoundTableMode(true);
    expect(getStore().roundTableMode).toBe(true);
    getStore().setRoundTableMode(false);
    expect(getStore().roundTableMode).toBe(false);
  });

  /* ── arrangeRoundTable ─────────────────────────────────── */

  it("places all agents in a circle", () => {
    getStore().addAgent("a1", "A", "bg-a");
    getStore().addAgent("a2", "B", "bg-b");
    getStore().addAgent("a3", "C", "bg-c");
    getStore().arrangeRoundTable(5, 0, 0);

    getStore().agents.forEach((agent) => {
      const [x, , z] = agent.targetPosition;
      const dist = Math.sqrt(x * x + z * z);
      expect(dist).toBeCloseTo(5, 0); // radius ≈ 5
    });
    expect(getStore().roundTableMode).toBe(true);
  });

  it("handles empty agent list gracefully", () => {
    expect(() => getStore().arrangeRoundTable(3, 0, 0)).not.toThrow();
  });

  /* ── scatterAgents ─────────────────────────────────────── */

  it("scatters agents randomly", () => {
    getStore().addAgent("a1", "A", "bg-a");
    getStore().addAgent("a2", "B", "bg-b");
    getStore().scatterAgents("seed", 10);
    expect(getStore().roundTableMode).toBe(false);
    getStore().agents.forEach((agent) => {
      const [x, , z] = agent.targetPosition;
      expect(Math.abs(x)).toBeLessThanOrEqual(5); // half of range
      expect(Math.abs(z)).toBeLessThanOrEqual(5);
    });
  });

  /* ── hash determinism ──────────────────────────────────── */

  it("produces same positions for same seed across resets", () => {
    resetStore();
    getStore().addAgent("seed", "Agent", "bg-x");
    const pos1 = getStore().agents.get("seed")!.position;

    resetStore();
    getStore().addAgent("seed", "Agent", "bg-y");
    const pos2 = getStore().agents.get("seed")!.position;

    expect(pos1).toEqual(pos2);
  });
});
