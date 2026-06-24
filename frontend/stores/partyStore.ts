"use client";

import { create } from "zustand";

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

/** Deterministic hash → number in [0, 1) from a string key. */
function hash(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h) / 0x7fffffff;
}

/** Seed a random-like number generator from a string. */
function seededRandom(seed: string, index: number): number {
  return hash(`${seed}-${index}`);
}

/** Compute a random-ish position inside a bounded room. */
function roomPosition(seed: string, index: number, range: number): [number, number, number] {
  const x = (seededRandom(seed, index * 3 + 0) - 0.5) * range;
  const z = (seededRandom(seed, index * 3 + 1) - 0.5) * range;
  return [x, 0, z];
}

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

export interface AgentEntry {
  id: string;
  name: string;
  position: [number, number, number]; // current (lerped)
  targetPosition: [number, number, number];
  color: string;
  mood: string;
}

interface PartyStore {
  agents: Map<string, AgentEntry>;
  userPosition: [number, number, number];
  roundTableMode: boolean;

  /* actions */
  addAgent: (id: string, name: string, color: string) => void;
  removeAgent: (id: string) => void;
  setAgentPosition: (id: string, pos: [number, number, number]) => void;
  setRoundTableMode: (on: boolean) => void;
  setMood: (id: string, mood: string) => void;

  /** Move all agents to positions around a circle of given radius. */
  arrangeRoundTable: (radius: number, centerX: number, centerZ: number) => void;
  /** Scatter agents randomly in the room. */
  scatterAgents: (seed: string, range: number) => void;
}

const USER_START: [number, number, number] = [0, 0, 5];

export const usePartyStore = create<PartyStore>((set, get) => ({
  agents: new Map(),
  userPosition: USER_START,
  roundTableMode: false,

  addAgent: (id, name, color) =>
    set((s) => {
      const agents = new Map(s.agents);
      if (agents.has(id)) return s; // already present
      const idx = agents.size;
      const pos = roomPosition(id, idx, 8);
      agents.set(id, { id, name, position: pos, targetPosition: pos, color, mood: "neutral" });
      return { agents };
    }),

  removeAgent: (id) =>
    set((s) => {
      const agents = new Map(s.agents);
      agents.delete(id);
      return { agents };
    }),

  setAgentPosition: (id, pos) =>
    set((s) => {
      const agent = s.agents.get(id);
      if (!agent) return s;
      const agents = new Map(s.agents);
      agents.set(id, { ...agent, targetPosition: pos });
      return { agents };
    }),

  setRoundTableMode: (on) => set({ roundTableMode: on }),

  setMood: (id, mood) =>
    set((s) => {
      const agent = s.agents.get(id);
      if (!agent) return s;
      const agents = new Map(s.agents);
      agents.set(id, { ...agent, mood });
      return { agents };
    }),

  arrangeRoundTable: (radius, cx, cz) =>
    set((s) => {
      const agents = new Map(s.agents);
      const ids = [...agents.keys()];
      ids.forEach((id, i) => {
        const angle = (2 * Math.PI * i) / ids.length - Math.PI / 2;
        const x = cx + radius * Math.cos(angle);
        const z = cz + radius * Math.sin(angle);
        const agent = agents.get(id);
        if (agent) agents.set(id, { ...agent, targetPosition: [x, 0, z] });
      });
      return { agents, roundTableMode: true };
    }),

  scatterAgents: (seed, range) =>
    set((s) => {
      const agents = new Map(s.agents);
      let idx = 0;
      agents.forEach((agent, id) => {
        const pos = roomPosition(id, idx++, range);
        agents.set(id, { ...agent, targetPosition: pos });
      });
      return { agents, roundTableMode: false };
    }),
}));
