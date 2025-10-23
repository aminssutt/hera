import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'

const themes = [
  { name: 'Animals', key: 'animals', emoji: '🦁', color: 'from-yellow-300 to-orange-400' },
  { name: 'Nature', key: 'nature', emoji: '🌳', color: 'from-green-300 to-green-500' },
  { name: 'Fantasy', key: 'fantasy', emoji: '🐉', color: 'from-purple-300 to-pink-400' },
  { name: 'Science', key: 'science', emoji: '🧪', color: 'from-blue-300 to-cyan-400' },
  { name: 'Transport', key: 'transport', emoji: '🚒', color: 'from-red-300 to-orange-400' },
  { name: 'Life', key: 'life', emoji: '🌱', color: 'from-teal-300 to-green-400' }
]

const StepOne = ({ selection, onSelect }) => {
  const { t } = useTranslation()
  
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
      <h2 className="text-2xl sm:text-3xl md:text-4xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4 text-center">
        {t('customize.chooseTheme')}
      </h2>
      <p className="text-center font-fredoka text-gray-500 mb-6 sm:mb-8 text-sm sm:text-base">
        {t('customize.selectThemes')}
      </p>
      
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4 md:gap-6">
        {themes.map((theme, index) => (
          <motion.div
            key={theme.name}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleThemeClick(theme.name)}
            className={`theme-card bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 text-center cursor-pointer shadow-lg
              ${selection.includes(theme.name) ? 'selected ring-2 sm:ring-4 ring-hera-purple ring-offset-2 sm:ring-offset-4' : 'hover:shadow-2xl'}
            `}
          >
            <div className={`text-4xl sm:text-5xl md:text-6xl mb-3 sm:mb-4 bg-gradient-to-br ${theme.color} w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto`}>
              {theme.emoji}
            </div>
            <h3 className="text-base sm:text-lg md:text-xl font-fredoka font-bold text-gray-700">
              {t(`themes.${theme.key}`)}
            </h3>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default StepOne
