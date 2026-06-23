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

  const replyMap = new Map<string, string>(); // message_id -> reply content

  for (const msg of messages) {
    if (msg.type === "chat:reply" && msg.message_id && msg.content) {
      replyMap.set(msg.message_id, msg.content);
    }
  }

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
          if (msg.type.startsWith("system:")) {
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

          // Regular chat message — agent message
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
