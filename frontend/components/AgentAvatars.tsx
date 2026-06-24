"use client";

import { usePartyStore } from "@/stores/partyStore";
import { AgentAvatar } from "./AgentAvatar";

/**
 * Maps Zustand store agents to AgentAvatar components.
 */
export function AgentAvatars() {
  const agents = usePartyStore((s) => s.agents);
  const userPosition = usePartyStore((s) => s.userPosition);

  return (
    <>
      {/* User avatar */}
      <AgentAvatar
        id="__user__"
        name="You"
        color="#94a3b8"
        position={userPosition}
        targetPosition={userPosition}
        isUser
      />

      {/* Agent avatars */}
      {[...agents.values()].map((agent) => (
        <AgentAvatar
          key={agent.id}
          id={agent.id}
          name={agent.name}
          color={agent.color}
          position={agent.position}
          targetPosition={agent.targetPosition}
        />
      ))}
    </>
  );
}
