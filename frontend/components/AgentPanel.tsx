"use client";

import { useState } from "react";

interface Agent {
  id: string;
  name: string;
  color: string;
  online: boolean;
}

const MOCK_AGENTS: Agent[] = [
  { id: "agent-1", name: "Aria", color: "bg-violet-500", online: true },
  { id: "agent-2", name: "Orion", color: "bg-cyan-500", online: true },
  { id: "agent-3", name: "Luna", color: "bg-pink-500", online: false },
];

interface AgentPanelProps {
  onPromptAgent: (agentId: string, prompt: string) => void;
}

export function AgentPanel({ onPromptAgent }: AgentPanelProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [prompts, setPrompts] = useState<Record<string, string>>({});

  const handlePromptChange = (agentId: string, value: string) => {
    setPrompts((prev) => ({ ...prev, [agentId]: value }));
  };

  const handlePrompt = () => {
    if (!expandedId) return;
    const text = prompts[expandedId] ?? "";
    if (!text.trim()) return;
    onPromptAgent(expandedId, text.trim());
    setPrompts((prev) => {
      const next = { ...prev };
      delete next[expandedId];
      return next;
    });
  };

  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Agents
      </h3>

      <div className="space-y-1 flex-1 overflow-y-auto">
        {MOCK_AGENTS.map((agent) => (
          <div key={agent.id}>
            <button
              onClick={() => setExpandedId(expandedId === agent.id ? null : agent.id)}
              className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm transition hover:bg-slate-800 ${
                expandedId === agent.id ? "bg-slate-800" : ""
              }`}
            >
              <span className={`w-6 h-6 rounded-full ${agent.color} flex items-center justify-center text-xs font-bold text-white`}>
                {agent.name[0]}
              </span>
              <span className="flex-1 text-left text-slate-200">{agent.name}</span>
              <span
                className={`w-2 h-2 rounded-full ${
                  agent.online ? "bg-emerald-400" : "bg-slate-600"
                }`}
              />
            </button>

            {expandedId === agent.id && (
              <div className="mx-2 mt-1 pb-2">
                <div className="flex gap-1">
                  <input
                    type="text"
                    value={prompts[agent.id] ?? ""}
                    onChange={(e) => handlePromptChange(agent.id, e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handlePrompt()}
                    placeholder={`Message ${agent.name}...`}
                    className="flex-1 px-2 py-1 text-xs rounded bg-slate-800 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500"
                  />
                  <button
                    onClick={handlePrompt}
                    disabled={!((prompts[agent.id] ?? "").trim())}
                    className="px-2 py-1 text-xs rounded bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white transition"
                  >
                    Send
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
