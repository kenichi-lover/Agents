"use client";

import { useState, useEffect } from "react";

const AGENT_COLORS: Record<string, string> = {
  "1": "bg-violet-500",
  "2": "bg-cyan-500",
  "3": "bg-pink-500",
};

interface Agent {
  id: string;
  name: string;
  color: string;
  online: boolean;
}

interface AgentPanelProps {
  onPromptAgent: (agentId: string, prompt: string) => void;
}

export function AgentPanel({ onPromptAgent }: AgentPanelProps) {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [prompts, setPrompts] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/agents")
      .then((r) => r.json())
      .then((data: any[]) => {
        setAgents(
          data.map((a, i) => ({
            id: a.id,
            name: a.name,
            color: AGENT_COLORS[String((i % 3) + 1)] ?? "bg-slate-500",
            online: true,
          }))
        );
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-slate-500 text-sm">
        Loading agents…
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Agents
      </h3>

      <div className="space-y-1 flex-1 overflow-y-auto">
        {agents.length === 0 && (
          <div className="text-xs text-slate-500 text-center py-4">No agents</div>
        )}
        {agents.map((agent) => (
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
