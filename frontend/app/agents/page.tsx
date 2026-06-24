"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface Agent {
  id: string;
  name: string;
  personality: string;
  expertise: string[];
  assertiveness: number;
}

export default function AgentsPage() {
  const router = useRouter();
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [personality, setPersonality] = useState("");
  const [expertise, setExpertise] = useState("");
  const [assertiveness, setAssertiveness] = useState(0.5);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetch("/api/agents")
      .then((r) => r.json())
      .then((data: Agent[]) => {
        setAgents(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [router]);

  const resetForm = () => {
    setName("");
    setPersonality("");
    setExpertise("");
    setAssertiveness(0.5);
    setShowForm(false);
    setEditingId(null);
    setError("");
  };

  const startCreate = () => {
    resetForm();
    setShowForm(true);
  };

  const startEdit = (agent: Agent) => {
    setEditingId(agent.id);
    setName(agent.name);
    setPersonality(agent.personality);
    setExpertise(agent.expertise.join(", "));
    setAssertiveness(agent.assertiveness);
    setShowForm(true);
  };

  const handleSave = async () => {
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const body = {
        name: name.trim(),
        personality: personality.trim() || "curious",
        expertise: expertise.split(",").map((s) => s.trim()).filter(Boolean),
        assertiveness: assertiveness,
      };
      const url = editingId
        ? `/api/agents/${editingId}`
        : "/api/agents";
      const method = editingId ? "PATCH" : "POST";
      const resp = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!resp.ok) throw new Error("Failed to save");
      const saved: Agent = await resp.json();
      setAgents((prev) =>
        editingId ? prev.map((a) => (a.id === editingId ? saved : a)) : [...prev, saved]
      );
      resetForm();
    } catch (e: any) {
      setError(e.message || "Failed to save agent");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this agent?")) return;
    try {
      const resp = await fetch(`/api/agents/${id}`, { method: "DELETE" });
      if (resp.ok) {
        setAgents((prev) => prev.filter((a) => a.id !== id));
      }
    } catch {
      // ignore
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center text-slate-400">
        Loading agents…
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Agents</h1>
          <button
            onClick={startCreate}
            className="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition"
          >
            + New Agent
          </button>
        </div>

        {/* Form */}
        {showForm && (
          <div className="bg-slate-800 rounded-xl p-4 mb-6 border border-slate-700">
            <h2 className="text-sm font-semibold mb-3">
              {editingId ? "Edit Agent" : "Create Agent"}
            </h2>
            {error && <p className="text-red-400 text-xs mb-2">{error}</p>}
            <div className="space-y-3">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Name *"
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500 text-sm"
              />
              <input
                type="text"
                value={personality}
                onChange={(e) => setPersonality(e.target.value)}
                placeholder="Personality (e.g. curious, witty)"
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500 text-sm"
              />
              <input
                type="text"
                value={expertise}
                onChange={(e) => setExpertise(e.target.value)}
                placeholder="Expertise (comma-separated)"
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-600 text-white placeholder-slate-500 outline-none focus:border-violet-500 text-sm"
              />
              <div>
                <label className="text-xs text-slate-400">
                  Assertiveness: {assertiveness.toFixed(1)}
                </label>
                <input
                  type="range"
                  min={0}
                  max={1}
                  step={0.1}
                  value={assertiveness}
                  onChange={(e) => setAssertiveness(parseFloat(e.target.value))}
                  className="w-full accent-violet-500"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 disabled:opacity-40 text-white text-sm font-medium transition"
                >
                  {saving ? "Saving…" : editingId ? "Save" : "Create"}
                </button>
                <button
                  onClick={resetForm}
                  className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-sm transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* List */}
        <div className="space-y-2">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="bg-slate-800 rounded-lg p-3 border border-slate-700 flex items-center gap-3"
            >
              <div className="w-8 h-8 rounded-full bg-violet-500 flex-shrink-0 flex items-center justify-center text-sm font-bold text-white">
                {agent.name[0]}
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-medium text-sm">{agent.name}</div>
                <div className="text-xs text-slate-400 truncate">
                  {agent.personality} · {agent.expertise.join(", ") || "general"}
                </div>
              </div>
              <button
                onClick={() => startEdit(agent)}
                className="px-2 py-1 text-xs rounded bg-slate-700 hover:bg-slate-600 text-slate-300 transition"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(agent.id)}
                className="px-2 py-1 text-xs rounded bg-red-900/50 hover:bg-red-900 text-red-300 transition"
              >
                Delete
              </button>
            </div>
          ))}
          {agents.length === 0 && (
            <p className="text-center text-slate-500 text-sm py-8">
              No agents yet — create one to get started.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
