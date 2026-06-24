"use client";

import { useEffect } from "react";
import { usePartyStore, type AgentEntry } from "@/stores/partyStore";

const AGENT_COLORS: Record<string, string> = {
  "1": "#8b5cf6", // violet
  "2": "#06b6d4", // cyan
  "3": "#ec4899", // pink
};

function getColorForIndex(index: number): string {
  return AGENT_COLORS[String((index % 3) + 1)] ?? "#64748b";
}

/**
 * Hook that bridges WebSocket messages to the Zustand 3D store.
 * Call this inside the party room page alongside useWebSocket.
 */
export function usePartyRoom(messages: Record<string, any>[]) {

  const addAgent = usePartyStore((s) => s.addAgent);
  const removeAgent = usePartyStore((s) => s.removeAgent);
  const setMood = usePartyStore((s) => s.setMood);

  useEffect(() => {
    const agentOrder = new Map<string, number>(); // track insertion order for colors

    for (const msg of messages) {
      if (!msg.type) continue;

      // system:join → add agent to 3D scene
      if (msg.type === "system:join" && msg.agent_id) {
        const idx = agentOrder.get(msg.agent_id) ?? agentOrder.size;
        agentOrder.set(msg.agent_id, idx);
        addAgent(msg.agent_id, msg.name ?? `Agent-${msg.agent_id.slice(0, 4)}`, getColorForIndex(idx));
      }

      // system:leave → remove agent
      if (msg.type === "system:leave" && msg.agent_id) {
        removeAgent(msg.agent_id);
      }

      // chat:reply → update mood
      if (msg.type === "chat:reply" && msg.agent_id && msg.mood) {
        setMood(msg.agent_id, msg.mood);
      }
    }
  }, [messages, addAgent, removeAgent, setMood]);
}
