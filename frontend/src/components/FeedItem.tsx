import type { FeedItem } from '../types'

interface Props {
  item: FeedItem
}

const sourceColors: Record<string, string> = {
  'BBC News': 'bg-red-900/50 text-red-300',
  Reuters: 'bg-orange-900/50 text-orange-300',
  CNN: 'bg-red-800/50 text-red-200',
  'Yahoo Finance': 'bg-purple-900/50 text-purple-300',
}

export default function FeedItem({ item }: Props) {
  const colorClass = sourceColors[item.source] ?? 'bg-gray-700 text-gray-300'
  const typeClass =
    item.type === 'market'
      ? 'bg-emerald-900/40 text-emerald-300'
      : 'bg-indigo-900/40 text-indigo-300'

  const formattedDate = item.published
    ? (() => {
        try {
          return new Date(item.published).toLocaleString()
        } catch {
          return item.published
        }
      })()
    : ''

  return (
    <article className="card hover:border-gray-700 transition-colors group">
      <div className="flex items-start gap-3">
        <span className="mt-1 text-xl flex-shrink-0">{item.type === 'market' ? '📊' : '📰'}</span>
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-1.5">
            <span className={`badge ${colorClass}`}>{item.source}</span>
            <span className={`badge ${typeClass}`}>{item.type}</span>
            {formattedDate && (
              <span className="text-gray-500 text-xs">{formattedDate}</span>
            )}
          </div>
          <a
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-white font-medium leading-snug hover:text-indigo-300 transition-colors line-clamp-2 block"
          >
            {item.title}
          </a>
          {item.summary && (
            <p className="mt-1.5 text-gray-400 text-sm line-clamp-2 leading-relaxed">
              {item.summary}
            </p>
          )}
        </div>
      </div>
    </article>
  )
}
