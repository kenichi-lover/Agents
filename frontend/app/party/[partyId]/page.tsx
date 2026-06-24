"use client";

import { use } from "react";
import { useEffect, useState } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { usePartyRoom } from "@/hooks/usePartyRoom";
import { ChatStream } from "@/components/ChatStream";
import { AgentPanel } from "@/components/AgentPanel";
import { PresenceBar } from "@/components/PresenceBar";
import { RoundTable } from "@/components/RoundTable";
import { PartyRoomScene } from "@/components/PartyRoomScene.client";

export default function PartyRoom({ params }: { params: Promise<{ partyId: string }> }) {
  const { partyId } = use(params);
  const [token, setToken] = useState("");

  useEffect(() => {
    setToken(localStorage.getItem("access_token") ?? "");
  }, []);

  const { isConnected, messages, sendMessage, sendStatus } = useWebSocket(partyId, token);

  // Bridge WebSocket messages to 3D Zustand store
  usePartyRoom(messages);

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
    <div className="relative h-screen w-full overflow-hidden bg-[#0f0a1a]">
      {/* 3D scene fills the entire viewport behind everything */}
      <PartyRoomScene partyId={partyId} />

      {/* UI overlay sits on top of the 3D scene */}
      <div className="absolute inset-0 flex flex-col pointer-events-none">
        <PresenceBar isConnected={isConnected} partyId={partyId} />

        <div className="flex-1 flex overflow-hidden pointer-events-none">
          <aside className="w-64 border-r border-slate-700/50 pointer-events-auto">
            <AgentPanel onPromptAgent={handlePromptAgent} />
          </aside>

          <main className="flex-1 flex flex-col">
            <ChatStream messages={messages} onSend={handleSendMessage} sendStatus={sendStatus} />
          </main>

          <aside className="w-80 border-l border-slate-700/50 pointer-events-auto">
            <RoundTable partyId={partyId} />
          </aside>
        </div>
      </div>
    </div>
  );
}
