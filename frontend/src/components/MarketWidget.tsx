import type { MarketData } from '../types'

interface Props {
  data: MarketData | null
  loading?: boolean
}

export default function MarketWidget({ data, loading }: Props) {
  if (loading) {
    return (
      <div className="card col-span-1">
        <div className="skeleton h-6 w-32 mb-3" />
        <div className="grid grid-cols-2 gap-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="skeleton h-16" />
          ))}
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="card col-span-1 flex items-center justify-center text-gray-500 min-h-[160px]">
        Market data unavailable
      </div>
    )
  }

  return (
    <div className="card col-span-1">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-white flex items-center gap-1.5">
          <span>📈</span> Markets
        </h2>
        <span className="text-gray-600 text-xs">Demo data</span>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {data.indices.map((idx) => {
          const isPositive = idx.change >= 0
          const changeClass = isPositive ? 'text-green-400' : 'text-red-400'
          const bgClass = isPositive ? 'bg-green-900/10' : 'bg-red-900/10'
          return (
            <div
              key={idx.name}
              className={`rounded-lg p-3 ${bgClass} border border-gray-800`}
            >
              <p className="text-gray-400 text-xs mb-1">{idx.name}</p>
              <p className="text-white font-bold text-lg leading-none">
                {idx.value.toLocaleString('en-US', { maximumFractionDigits: 2 })}
              </p>
              <p className={`text-xs mt-1 font-medium ${changeClass}`}>
                {isPositive ? '▲' : '▼'} {Math.abs(idx.change_percent).toFixed(2)}%
              </p>
            </div>
          )
        })}
      </div>
    </div>
  )
}
