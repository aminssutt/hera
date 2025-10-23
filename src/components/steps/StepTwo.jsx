import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'

const topics = [
  { name: 'Ghibli', key: 'ghibli', description: 'Studio Ghibli inspired', emoji: '🎨' },
  { name: 'Cartoon', key: 'cartoon', description: 'Fun cartoon style', emoji: '😄' },
  { name: 'Minimal', key: 'minimal', description: 'Simple & clean', emoji: '⭕' },
  { name: 'Comic', key: 'comic', description: 'Comic book style', emoji: '💥' },
  { name: 'Detailed', key: 'detailed', description: 'Rich in details', emoji: '🔍' },
  { name: 'Magical', key: 'magical', description: 'Mystical & enchanting', emoji: '✨' }
]

const StepTwo = ({ selection, onSelect }) => {
  const { t } = useTranslation()
  
  return (
    <div>
      <h2 className="text-2xl sm:text-3xl md:text-4xl font-fredoka font-bold text-gray-700 mb-6 sm:mb-8 text-center">
        {t('customize.chooseArtStyle')}
      </h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        {topics.map((topic, index) => (
          <motion.div
            key={topic.name}
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05, rotate: 2 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onSelect(topic.name)}
            className={`topic-card bg-white rounded-2xl sm:rounded-3xl p-6 sm:p-8 text-center cursor-pointer shadow-lg
              ${selection === topic.name ? 'selected ring-2 sm:ring-4 ring-hera-blue ring-offset-2 sm:ring-offset-4' : 'hover:shadow-2xl'}
            `}
          >
            <div className="text-5xl sm:text-6xl md:text-7xl mb-3 sm:mb-4">
              {topic.emoji}
            </div>
            <h3 className="text-xl sm:text-2xl font-fredoka font-bold text-gray-700 mb-2">
              {t(`styles.${topic.key}`)}
            </h3>
            <p className="text-sm sm:text-base text-gray-500 font-fredoka">
              {t(`styles.${topic.key}Desc`)}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default StepTwo
