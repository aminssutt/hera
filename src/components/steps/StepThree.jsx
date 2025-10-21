import { motion } from 'framer-motion'
import { useState } from 'react'

const difficulties = ['Easy', 'Medium', 'Hard']

// Organized color palettes
const colorPalettes = {
  warm: {
    name: '🔥 Warm Colors',
    colors: [
      { hex: '#FF6B6B', name: 'Red' },
      { hex: '#FF8E3C', name: 'Orange' },
      { hex: '#FFA500', name: 'Deep Orange' },
      { hex: '#FFD93D', name: 'Gold' },
      { hex: '#FF6F91', name: 'Coral' },
      { hex: '#FF9AA2', name: 'Salmon' },
      { hex: '#FFB347', name: 'Peach' }
    ]
  },
  cold: {
    name: '❄️ Cold Colors',
    colors: [
      { hex: '#4A90E2', name: 'Blue' },
      { hex: '#5EB3E4', name: 'Sky Blue' },
      { hex: '#00D4FF', name: 'Cyan' },
      { hex: '#4ECDC4', name: 'Teal' },
      { hex: '#7B68EE', name: 'Purple' },
      { hex: '#6A5ACD', name: 'Slate Blue' },
      { hex: '#20B2AA', name: 'Turquoise' }
    ]
  },
  pastel: {
    name: '🌸 Pastel Colors',
    colors: [
      { hex: '#FFB6C1', name: 'Light Pink' },
      { hex: '#E0BBE4', name: 'Lavender' },
      { hex: '#B4E7CE', name: 'Mint' },
      { hex: '#FFE4E1', name: 'Misty Rose' },
      { hex: '#FFDFD3', name: 'Peach Cream' },
      { hex: '#C7CEEA', name: 'Periwinkle' },
      { hex: '#FFF5BA', name: 'Lemon Cream' }
    ]
  },
  classic: {
    name: '🖤 Natural & Neutral Colors',
    colors: [
      { hex: '#2C2C2C', name: 'Charcoal' },
      { hex: '#5A5A5A', name: 'Dark Gray' },
      { hex: '#8B8B8B', name: 'Gray' },
      { hex: '#A0826D', name: 'Brown' },
      { hex: '#8B4513', name: 'Saddle Brown' },
      { hex: '#D2B48C', name: 'Tan' },
      { hex: '#F5F5DC', name: 'Beige' }
    ]
  }
}

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
          🎨 Color Palette (Select any colors)
        </h3>
        <p className="text-sm sm:text-base font-fredoka text-gray-600 mb-4">
          Choose colors from any palette below - they'll be used to color your book!
        </p>
        
        {/* Color Palettes */}
        <div className="space-y-6">
          {Object.entries(colorPalettes).map(([key, palette]) => (
            <div key={key}>
              <h4 className="text-base sm:text-lg font-fredoka font-bold text-gray-600 mb-3">
                {palette.name}
              </h4>
              <div className="grid grid-cols-7 gap-2 sm:gap-3">
                {palette.colors.map((color) => (
                  <motion.button
                    key={color.hex}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => toggleColor(color.hex)}
                    className={`relative aspect-square rounded-xl sm:rounded-2xl transition-all shadow-md
                      ${selectedColors.includes(color.hex) 
                        ? 'ring-2 sm:ring-4 ring-gray-800 ring-offset-2 shadow-xl' 
                        : 'hover:shadow-lg'
                      }
                    `}
                    style={{ backgroundColor: color.hex }}
                    title={color.name}
                  >
                    {selectedColors.includes(color.hex) && (
                      <span className="absolute inset-0 flex items-center justify-center text-white text-xl sm:text-2xl font-bold drop-shadow-lg">
                        ✓
                      </span>
                    )}
                  </motion.button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Selected Colors Summary */}
        {selectedColors.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-6 p-4 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl"
          >
            <p className="text-sm font-fredoka font-bold text-gray-700 mb-2">
              ✨ Selected Colors ({selectedColors.length}):
            </p>
            <div className="flex flex-wrap gap-2">
              {selectedColors.map((color) => (
                <div
                  key={color}
                  className="w-8 h-8 rounded-lg shadow-md border-2 border-white"
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>
          </motion.div>
        )}
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
