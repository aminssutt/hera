import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Customize from './pages/Customize'
import AnimatedBackground from './components/AnimatedBackground'
import './index.css'

function App() {
  return (
    <Router>
      <div className="relative min-h-screen">
        <AnimatedBackground />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/customize" element={<Customize />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
