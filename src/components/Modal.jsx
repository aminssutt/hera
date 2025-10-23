import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'

const Modal = ({ isOpen, onClose, onConfirm, title, message }) => {
  const { t } = useTranslation()
  if (!isOpen) return null

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.8, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-white rounded-3xl p-8 max-w-md mx-4 shadow-2xl"
        >
          <div className="text-center mb-6">
            <div className="text-6xl mb-4">⚠️</div>
            <h2 className="text-3xl font-bubblegum text-gray-700 mb-2">
              {title}
            </h2>
            <p className="text-lg font-fredoka text-gray-600">
              {message}
            </p>
          </div>

          <div className="flex gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onClose}
              className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 font-fredoka font-bold text-xl py-4 rounded-2xl transition-all"
            >
              {t('modal.noStay')}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onConfirm}
              className="flex-1 bg-gradient-magical text-white font-fredoka font-bold text-xl py-4 rounded-2xl transition-all shadow-lg"
            >
              {t('modal.yesLeave')}
            </motion.button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}

export default Modal
