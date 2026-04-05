import { useState } from 'react'
import { useAgentData } from '../hooks/useAgentData'
import WeatherWidget from '../components/WeatherWidget'
import MarketWidget from '../components/MarketWidget'
import AgentCard from '../components/AgentCard'
import FeedItemComp from '../components/FeedItem'

export default function Dashboard() {
  const { agents, feed, weather, marketData, loading, error, refresh, runAgent } = useAgentData()
  const [runningAgent, setRunningAgent] = useState<string | null>(null)
  const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date())

  const handleRefresh = () => {
    refresh()
    setLastRefreshed(new Date())
  }

  const handleRunAgent = async (name: string) => {
    setRunningAgent(name)
    try {
      await runAgent(name)
    } finally {
      setRunningAgent(null)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 text-sm mt-0.5">
            Your AI-powered world intelligence feed
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-gray-500 text-xs">
            Updated {lastRefreshed.toLocaleTimeString()}
          </span>
          <button className="btn-primary" onClick={handleRefresh} disabled={loading}>
            {loading ? '⟳ Refreshing…' : '⟳ Refresh'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-800 text-red-300 rounded-xl p-4 text-sm">
          ⚠️ {error} — Make sure the backend is running on port 8000.
        </div>
      )}

      {/* Widgets row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <WeatherWidget data={weather} loading={loading && !weather} />
        <MarketWidget data={marketData} loading={loading && !marketData} />
      </div>

      {/* Agent status */}
      <div>
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
          Active Agents
        </h2>
        {loading && agents.length === 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="skeleton h-32" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <AgentCard
                key={agent.name}
                agent={agent}
                onRun={handleRunAgent}
                running={runningAgent === agent.name}
              />
            ))}
          </div>
        )}
      </div>

      {/* Feed */}
      <div>
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
          Live Feed{' '}
          {feed.length > 0 && (
            <span className="text-indigo-400 normal-case font-normal">
              ({feed.length} items)
            </span>
          )}
        </h2>

        {loading && feed.length === 0 ? (
          <div className="space-y-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="skeleton h-24" />
            ))}
          </div>
        ) : feed.length === 0 ? (
          <div className="card text-gray-500 text-center py-12">
            No feed items yet. Click <strong>Refresh</strong> or run individual agents.
          </div>
        ) : (
          <div className="space-y-3">
            {feed.map((item, idx) => (
              <FeedItemComp key={`${item.link}-${idx}`} item={item} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
