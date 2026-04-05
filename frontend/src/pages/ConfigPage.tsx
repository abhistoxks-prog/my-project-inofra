import { useState, useEffect } from 'react'
import { useAgentData } from '../hooks/useAgentData'

const LOCATION_PRESETS = [
  { name: 'New York', lat: 40.71, lon: -74.01 },
  { name: 'London', lat: 51.51, lon: -0.13 },
  { name: 'Tokyo', lat: 35.68, lon: 139.69 },
  { name: 'Sydney', lat: -33.87, lon: 151.21 },
  { name: 'Paris', lat: 48.85, lon: 2.35 },
  { name: 'Dubai', lat: 25.20, lon: 55.27 },
]

export default function ConfigPage() {
  const { config, saveConfig, loading } = useAgentData()
  const [topicsInput, setTopicsInput] = useState('')
  const [selectedLocation, setSelectedLocation] = useState('New York')
  const [refreshInterval, setRefreshInterval] = useState(300)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (config) {
      setTopicsInput(config.topics.join(', '))
      setSelectedLocation(config.location.name)
      setRefreshInterval(config.refresh_interval)
    }
  }, [config])

  const handleSave = async () => {
    const topics = topicsInput
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean)
    const loc = LOCATION_PRESETS.find((l) => l.name === selectedLocation) ??
      LOCATION_PRESETS[0]

    await saveConfig({
      topics,
      location: { lat: loc.lat, lon: loc.lon, name: loc.name },
      refresh_interval: refreshInterval,
    })
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-gray-400 text-sm mt-0.5">
          Configure your intelligence feed
        </p>
      </div>

      {saved && (
        <div className="bg-green-900/30 border border-green-800 text-green-300 rounded-xl px-4 py-3 text-sm">
          ✅ Settings saved successfully.
        </div>
      )}

      {/* Topics */}
      <div className="card space-y-3">
        <h2 className="font-semibold text-white">News Topics</h2>
        <p className="text-gray-400 text-sm">
          Filter news articles by keywords. Leave blank to see all news.
        </p>
        <input
          type="text"
          value={topicsInput}
          onChange={(e) => setTopicsInput(e.target.value)}
          placeholder="e.g. technology, AI, climate, finance"
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white placeholder-gray-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <p className="text-gray-600 text-xs">Comma-separated keywords</p>
      </div>

      {/* Location */}
      <div className="card space-y-3">
        <h2 className="font-semibold text-white">Weather Location</h2>
        <p className="text-gray-400 text-sm">
          Choose a city for your weather forecast.
        </p>
        <div className="grid grid-cols-3 gap-2">
          {LOCATION_PRESETS.map((loc) => (
            <button
              key={loc.name}
              onClick={() => setSelectedLocation(loc.name)}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors border ${
                selectedLocation === loc.name
                  ? 'bg-indigo-600/30 border-indigo-500 text-indigo-200'
                  : 'bg-gray-800 border-gray-700 text-gray-300 hover:border-gray-600'
              }`}
            >
              {loc.name}
            </button>
          ))}
        </div>
      </div>

      {/* Refresh interval */}
      <div className="card space-y-3">
        <h2 className="font-semibold text-white">Auto-refresh Interval</h2>
        <p className="text-gray-400 text-sm">
          How often agents automatically refresh data.
        </p>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min={60}
            max={1800}
            step={60}
            value={refreshInterval}
            onChange={(e) => setRefreshInterval(Number(e.target.value))}
            className="flex-1 accent-indigo-500"
          />
          <span className="text-white font-medium w-20 text-right">
            {refreshInterval >= 60
              ? `${Math.round(refreshInterval / 60)} min`
              : `${refreshInterval}s`}
          </span>
        </div>
      </div>

      <button
        className="btn-primary w-full py-2.5 text-base"
        onClick={handleSave}
        disabled={loading}
      >
        Save Settings
      </button>
    </div>
  )
}
