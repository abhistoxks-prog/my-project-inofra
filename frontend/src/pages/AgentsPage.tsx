import { useState } from 'react'
import { useAgentData } from '../hooks/useAgentData'
import AgentCard from '../components/AgentCard'

export default function AgentsPage() {
  const { agents, loading, runAgent } = useAgentData()
  const [runningAgent, setRunningAgent] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  const handleRun = async (name: string) => {
    setRunningAgent(name)
    setMessage(null)
    try {
      await runAgent(name)
      setMessage(`✅ Agent "${name}" completed successfully.`)
    } catch {
      setMessage(`❌ Agent "${name}" encountered an error.`)
    } finally {
      setRunningAgent(null)
      setTimeout(() => setMessage(null), 4000)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Agents</h1>
        <p className="text-gray-400 text-sm mt-0.5">
          Manage and monitor your AI agents
        </p>
      </div>

      {message && (
        <div className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-sm text-gray-200">
          {message}
        </div>
      )}

      {loading && agents.length === 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="skeleton h-40" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {agents.map((agent) => (
            <AgentCard
              key={agent.name}
              agent={agent}
              onRun={handleRun}
              running={runningAgent === agent.name}
            />
          ))}
        </div>
      )}

      {/* Legend */}
      <div className="card">
        <h3 className="font-semibold text-white mb-3">Agent Status Legend</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
          {[
            { label: 'Idle', classes: 'bg-gray-700 text-gray-300', desc: 'Waiting for trigger' },
            { label: 'Running', classes: 'bg-blue-900/50 text-blue-300', desc: 'Fetching data now' },
            { label: 'Active', classes: 'bg-green-900/50 text-green-300', desc: 'Data is fresh' },
            { label: 'Error', classes: 'bg-red-900/50 text-red-300', desc: 'Fetch failed' },
          ].map((s) => (
            <div key={s.label} className="flex items-center gap-2">
              <span className={`badge ${s.classes}`}>{s.label}</span>
              <span className="text-gray-500 text-xs">{s.desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
