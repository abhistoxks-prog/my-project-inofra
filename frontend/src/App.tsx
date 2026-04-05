import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import AgentsPage from './pages/AgentsPage'
import ConfigPage from './pages/ConfigPage'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/agents" element={<AgentsPage />} />
            <Route path="/settings" element={<ConfigPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
