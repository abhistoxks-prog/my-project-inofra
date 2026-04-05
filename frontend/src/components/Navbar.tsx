import { Link, useLocation } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/agents', label: 'Agents' },
  { to: '/settings', label: 'Settings' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="sticky top-0 z-50 bg-gray-950/90 backdrop-blur border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-2 font-bold text-lg tracking-tight">
          <span className="text-2xl">🧠</span>
          <span className="text-white">WorldWatch</span>
          <span className="text-indigo-400">AI</span>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-1">
          {links.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                pathname === to
                  ? 'bg-indigo-600/20 text-indigo-300'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Online indicator */}
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500" />
          </span>
          Online
        </div>
      </div>
    </nav>
  )
}
