import { useState, useEffect, useCallback, useRef } from 'react'
import axios from 'axios'
import type { Agent, FeedItem, WeatherData, MarketData, Config } from '../types'

const API_BASE = import.meta.env.VITE_API_URL ?? ''

export function useAgentData() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [feed, setFeed] = useState<FeedItem[]>([])
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [marketData, setMarketData] = useState<MarketData | null>(null)
  const [config, setConfig] = useState<Config | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const fetchAll = useCallback(async () => {
    try {
      setError(null)
      const [agentsRes, feedRes, weatherRes, configRes] = await Promise.allSettled([
        axios.get(`${API_BASE}/api/agents`),
        axios.get(`${API_BASE}/api/feed`),
        axios.get(`${API_BASE}/api/weather`),
        axios.get(`${API_BASE}/api/config`),
      ])

      if (agentsRes.status === 'fulfilled') {
        setAgents(agentsRes.value.data.agents ?? [])
      }
      if (feedRes.status === 'fulfilled') {
        setFeed(feedRes.value.data.items ?? [])
      }
      if (weatherRes.status === 'fulfilled') {
        setWeather(weatherRes.value.data)
      }
      if (configRes.status === 'fulfilled') {
        setConfig(configRes.value.data)
        const mktResult = await axios.get(`${API_BASE}/api/agents/market/results`).catch(() => null)
        if (mktResult) setMarketData(mktResult.data.result)
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch data'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }, [])

  const refresh = useCallback(() => {
    setLoading(true)
    fetchAll()
  }, [fetchAll])

  const runAgent = useCallback(async (name: string) => {
    await axios.get(`${API_BASE}/api/agents/${name}/run`)
    await fetchAll()
  }, [fetchAll])

  const saveConfig = useCallback(async (updates: Partial<Config>) => {
    await axios.post(`${API_BASE}/api/config`, updates)
    const res = await axios.get(`${API_BASE}/api/config`)
    setConfig(res.data)
  }, [])

  useEffect(() => {
    fetchAll()
    intervalRef.current = setInterval(fetchAll, 5 * 60 * 1000)
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [fetchAll])

  return { agents, feed, weather, marketData, config, loading, error, refresh, runAgent, saveConfig }
}
