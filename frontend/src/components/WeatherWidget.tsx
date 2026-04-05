import type { WeatherData } from '../types'

interface Props {
  data: WeatherData | null
  loading?: boolean
}

function weatherEmoji(code: number): string {
  if (code === 0) return '☀️'
  if (code <= 2) return '🌤️'
  if (code === 3) return '☁️'
  if (code <= 48) return '🌫️'
  if (code <= 67) return '🌧️'
  if (code <= 77) return '❄️'
  if (code <= 82) return '🌦️'
  if (code <= 86) return '🌨️'
  return '⛈️'
}

export default function WeatherWidget({ data, loading }: Props) {
  if (loading) {
    return (
      <div className="card col-span-1">
        <div className="skeleton h-6 w-32 mb-3" />
        <div className="skeleton h-16 w-24 mb-4" />
        <div className="flex gap-2">
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="skeleton h-16 flex-1" />
          ))}
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="card col-span-1 flex items-center justify-center text-gray-500 min-h-[160px]">
        Weather unavailable
      </div>
    )
  }

  const { current, daily, location } = data
  const emoji = weatherEmoji(current.weather_code)

  return (
    <div className="card col-span-1">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-white flex items-center gap-1.5">
          <span>🌍</span> Weather
        </h2>
        <span className="text-gray-400 text-sm">{location}</span>
      </div>

      {/* Current */}
      <div className="flex items-center gap-4 mb-4">
        <span className="text-5xl">{emoji}</span>
        <div>
          <p className="text-4xl font-bold text-white">
            {current.temperature != null ? `${Math.round(current.temperature)}°C` : '—'}
          </p>
          <p className="text-gray-400 text-sm">{current.weather_description}</p>
          <p className="text-gray-500 text-xs mt-0.5">
            💨 {current.wind_speed != null ? `${current.wind_speed} km/h` : '—'}
          </p>
        </div>
      </div>

      {/* 7-day forecast */}
      <div className="grid grid-cols-7 gap-1">
        {daily.slice(0, 7).map((day) => (
          <div
            key={day.date}
            className="flex flex-col items-center gap-0.5 bg-gray-800/50 rounded-lg py-2 px-1"
          >
            <span className="text-gray-400 text-xs">
              {new Date(day.date + 'T00:00:00').toLocaleDateString('en', { weekday: 'short' })}
            </span>
            <span className="text-sm font-medium text-white">
              {day.temp_max != null ? `${Math.round(day.temp_max)}°` : '—'}
            </span>
            <span className="text-xs text-gray-500">
              {day.temp_min != null ? `${Math.round(day.temp_min)}°` : '—'}
            </span>
            {day.precipitation != null && day.precipitation > 0 && (
              <span className="text-xs text-blue-400">{day.precipitation}mm</span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
