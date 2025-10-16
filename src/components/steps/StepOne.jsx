import { motion } from 'framer-motion'

const themes = [
  { name: 'Animals', emoji: '🦁', color: 'from-yellow-300 to-orange-400' },
  { name: 'Nature', emoji: '🌳', color: 'from-green-300 to-green-500' },
  { name: 'Fantasy', emoji: '🐉', color: 'from-purple-300 to-pink-400' },
  { name: 'Science', emoji: '🧪', color: 'from-blue-300 to-cyan-400' },
  { name: 'Transport', emoji: '🚒', color: 'from-red-300 to-orange-400' },
  { name: 'Life', emoji: '🌱', color: 'from-teal-300 to-green-400' }
]

const StepOne = ({ selection, onSelect }) => {
  const handleThemeClick = (themeName) => {
    // If already selected, deselect it
    if (selection.includes(themeName)) {
      onSelect(selection.filter(t => t !== themeName))
    } else {
      // If less than 2 themes selected, add it
      if (selection.length < 2) {
        onSelect([...selection, themeName])
      } else {
        // Replace the first one if already have 2
        onSelect([selection[1], themeName])
      }
    }
  }

  return (
    <div>
      <h2 className="text-4xl font-fredoka font-bold text-gray-700 mb-4 text-center">
        Choose Your Theme(s)
      </h2>
      <p className="text-center font-fredoka text-gray-500 mb-8">
        Select 1 or 2 themes for your coloring book
      </p>
      
      <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
        {themes.map((theme, index) => (
          <motion.div
            key={theme.name}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleThemeClick(theme.name)}
            className={`theme-card bg-white rounded-3xl p-6 text-center cursor-pointer shadow-lg
              ${selection.includes(theme.name) ? 'selected ring-4 ring-hera-purple ring-offset-4' : 'hover:shadow-2xl'}
            `}
          >
            <div className={`text-6xl mb-4 bg-gradient-to-br ${theme.color} w-24 h-24 rounded-2xl flex items-center justify-center mx-auto`}>
              {theme.emoji}
            </div>
            <h3 className="text-xl font-fredoka font-bold text-gray-700">
              {theme.name}
            </h3>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default StepOne
