"use client";

import { use } from "react";
import { useEffect, useState } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { ChatStream } from "@/components/ChatStream";
import { AgentPanel } from "@/components/AgentPanel";
import { PresenceBar } from "@/components/PresenceBar";
import { RoundTable } from "@/components/RoundTable";

export default function PartyRoom({ params }: { params: Promise<{ partyId: string }> }) {
  const { partyId } = use(params);
  const [token, setToken] = useState("");

  useEffect(() => {
    setToken(localStorage.getItem("access_token") ?? "");
  }, []);

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
