import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Customize from './pages/Customize'
import Success from './pages/Success'
import Cancel from './pages/Cancel'
import Contact from './pages/Contact'
import AnimatedBackground from './components/AnimatedBackground'
import LanguageSwitcher from './components/LanguageSwitcher'
import './index.css'

function App() {
  return (
    <Router>
      <div className="relative min-h-screen">
        <AnimatedBackground />
        <LanguageSwitcher />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/customize" element={<Customize />} />
          <Route path="/success" element={<Success />} />
          <Route path="/cancel" element={<Cancel />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
