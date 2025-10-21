import { motion } from 'framer-motion'
import { useState } from 'react'

const difficulties = ['Easy', 'Medium', 'Hard']
const colorOptions = [
  '#FFAA7A', // Orange
  '#7FD687', // Green
  '#E891C8', // Pink
  '#5EB3E4', // Blue
  '#FFE347', // Yellow
  '#A97DC0', // Purple
  '#FF6B9D', // Rose
  '#4ECDC4'  // Teal
]

const StepThree = ({ selections, onUpdate }) => {
  const [selectedColors, setSelectedColors] = useState(selections.colors || [])

  const toggleColor = (color) => {
    let newColors
    if (selectedColors.includes(color)) {
      newColors = selectedColors.filter(c => c !== color)
    } else {
      newColors = [...selectedColors, color]
    }
    setSelectedColors(newColors)
    onUpdate('colors', newColors)
  }

  return (
    <div className="space-y-6 sm:space-y-8">
      {/* Pages Section */}
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 shadow-lg"
      >
        <h3 className="text-xl sm:text-2xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
          📄 Number of Pages
        </h3>
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:gap-4">
          <span className="text-3xl sm:text-4xl font-fredoka font-bold text-hera-purple min-w-[60px]">
            {selections.pages}
          </span>
          <input
            type="range"
            min="10"
            max="20"
            step="2"
            value={selections.pages}
            onChange={(e) => onUpdate('pages', parseInt(e.target.value))}
            className="flex-1 h-3 w-full"
          />
          <div className="flex gap-2 text-xs sm:text-sm font-fredoka text-gray-500 self-end sm:self-auto">
            <span>10</span>
            <span>20</span>
          </div>
        </div>
        
      </motion.div>

      {/* Difficulty Section */}
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 shadow-lg"
      >
        <h3 className="text-xl sm:text-2xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
          🎯 Difficulty Level
        </h3>
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
          {difficulties.map((diff) => (
            <motion.button
              key={diff}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onUpdate('difficulty', diff)}
              className={`flex-1 py-3 sm:py-4 px-4 sm:px-6 rounded-xl sm:rounded-2xl font-fredoka font-bold text-lg sm:text-xl transition-all
                ${selections.difficulty === diff
                  ? 'bg-gradient-magical text-white shadow-xl'
                  : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                }
              `}
            >
              {diff}
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Colors Section */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 shadow-lg"
      >
        <h3 className="text-xl sm:text-2xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
          🎨 Color Theme (Select multiple)
        </h3>
        <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-3 sm:gap-4">
          {colorOptions.map((color) => (
            <motion.button
              key={color}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => toggleColor(color)}
              className={`w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-xl sm:rounded-2xl transition-all shadow-md
                ${selectedColors.includes(color) 
                  ? 'ring-2 sm:ring-4 ring-gray-700 ring-offset-2 shadow-xl' 
                  : 'hover:shadow-xl'
                }
              `}
              style={{ backgroundColor: color }}
            >
              {selectedColors.includes(color) && (
                <span className="text-white text-xl sm:text-2xl">✓</span>
              )}
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Preview Badge */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4 }}
        className="bg-gradient-magical text-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 text-center"
      >
        <h3 className="text-2xl sm:text-3xl font-bubblegum mb-2">
          🎉 Your Book is Ready!
        </h3>
        <p className="font-fredoka text-base sm:text-lg">
          {selections.pages} pages • {selections.difficulty} level • {selectedColors.length} colors
        </p>
      </motion.div>
    </div>
  )
}

export default StepThree
