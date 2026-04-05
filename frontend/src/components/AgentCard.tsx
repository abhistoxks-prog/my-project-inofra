import type { Agent } from '../types'

interface Props {
  agent: Agent
  onRun: (name: string) => void
  running?: boolean
}

const statusConfig = {
  idle: { label: 'Idle', classes: 'bg-gray-700 text-gray-300' },
  running: { label: 'Running', classes: 'bg-blue-900/50 text-blue-300 animate-pulse' },
  error: { label: 'Error', classes: 'bg-red-900/50 text-red-300' },
  success: { label: 'Active', classes: 'bg-green-900/50 text-green-300' },
}

const agentIcons: Record<string, string> = {
  news: '📰',
  weather: '🌤️',
  market: '📈',
}

export default function AgentCard({ agent, onRun, running }: Props) {
  const cfg = statusConfig[agent.status] ?? statusConfig.idle
  const icon = agentIcons[agent.name] ?? '🤖'
  const lastUpdated = agent.last_updated
    ? new Date(agent.last_updated + 'Z').toLocaleTimeString()
    : 'Never'

  return (
    <div className="card flex flex-col gap-3">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{icon}</span>
          <div>
            <h3 className="font-semibold capitalize text-white">{agent.name}</h3>
            <span className={`badge ${cfg.classes}`}>{cfg.label}</span>
          </div>
        </div>
        <button
          className="btn-primary"
          onClick={() => onRun(agent.name)}
          disabled={running || agent.status === 'running'}
        >
          {running || agent.status === 'running' ? 'Running…' : 'Run'}
        </button>
      </div>
      <p className="text-gray-400 text-sm">{agent.description}</p>
      <p className="text-gray-600 text-xs">Last updated: {lastUpdated}</p>
    </div>
  )
}
