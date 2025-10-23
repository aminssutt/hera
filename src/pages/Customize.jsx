import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import StepOne from '../components/steps/StepOne'
import StepTwo from '../components/steps/StepTwo'
import StepThree from '../components/steps/StepThree'
import StepFour from '../components/steps/StepFour'
import Modal from '../components/Modal'

const Customize = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(1)
  const [showModal, setShowModal] = useState(false)
  const [selections, setSelections] = useState({
    theme: [],
    topic: '',
    pages: 12,
    difficulty: 'Easy',
    colors: []
  })

  const updateSelection = (field, value) => {
    setSelections(prev => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (currentStep < 4) {
      setCurrentStep(prev => prev + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1)
    }
  }

  const slideVariants = {
    enter: (direction) => ({
      x: direction > 0 ? 1000 : -1000,
      opacity: 0
    }),
    center: {
      x: 0,
      opacity: 1
    },
    exit: (direction) => ({
      x: direction < 0 ? 1000 : -1000,
      opacity: 0
    })
  }

  const [direction, setDirection] = useState(0)

  const handleNext = () => {
    setDirection(1)
    nextStep()
  }

  const handleBack = () => {
    setDirection(-1)
    prevStep()
  }

  const handleHomeClick = () => {
    setShowModal(true)
  }

  const handleConfirmExit = () => {
    setShowModal(false)
    navigate('/')
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-3 sm:p-4 md:p-8">
      <div className="w-full max-w-7xl">
        {/* Modal */}
        <Modal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          onConfirm={handleConfirmExit}
          title={t('customize.modalTitle')}
          message={t('customize.modalMessage')}
        />

        {/* Header */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="flex items-center justify-between mb-6 sm:mb-8"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleHomeClick}
            className="bg-white/70 backdrop-blur-sm hover:bg-white/90 text-gray-700 font-fredoka font-bold px-4 sm:px-6 py-2 sm:py-3 rounded-full shadow-lg transition-all flex items-center gap-1 sm:gap-2 text-sm sm:text-base"
          >
            <span className="text-xl sm:text-2xl">🏠</span>
            <span className="hidden sm:inline">{t('customize.home')}</span>
          </motion.button>
          
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bubblegum text-gray-700">Hēra</h1>
          
          <div className="w-16 sm:w-24 md:w-32"></div> {/* Spacer for centering */}
        </motion.div>

        <div className="flex flex-col lg:flex-row gap-4 sm:gap-6">
          {/* Sidebar - Steps Indicator (Hidden on mobile, shown on lg+) */}
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="hidden lg:block lg:w-80 bg-white/60 backdrop-blur-sm rounded-3xl p-6 shadow-xl"
          >
            {/* Step 1 */}
            <div className={`mb-6 p-4 rounded-2xl transition-all ${currentStep === 1 ? 'bg-gradient-magical' : 'bg-gray-200'}`}>
              <h3 className={`text-xl font-fredoka font-bold mb-2 ${currentStep === 1 ? 'text-white' : 'text-gray-500'}`}>
                {t('customize.step')} 1
              </h3>
              {selections.theme.length > 0 && (
                <div className="space-y-2">
                  {selections.theme.map((theme, idx) => (
                    <div key={idx} className="bg-white rounded-xl p-3 flex items-center gap-2">
                      <span className="text-2xl">{getThemeEmoji(theme)}</span>
                      <span className="font-fredoka text-sm">{theme}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Step 2 */}
            <div className={`mb-6 p-4 rounded-2xl transition-all ${currentStep === 2 ? 'bg-gradient-magical' : 'bg-gray-200'}`}>
              <h3 className={`text-xl font-fredoka font-bold mb-2 ${currentStep === 2 ? 'text-white' : 'text-gray-500'}`}>
                {t('customize.step')} 2
              </h3>
              {selections.topic && (
                <div className="bg-white rounded-xl p-3">
                  <span className="font-fredoka text-sm">{selections.topic}</span>
                </div>
              )}
            </div>

            {/* Step 3 */}
            <div className={`mb-6 p-4 rounded-2xl transition-all ${currentStep === 3 ? 'bg-gradient-magical' : 'bg-gray-200'}`}>
              <h3 className={`text-xl font-fredoka font-bold mb-2 ${currentStep === 3 ? 'text-white' : 'text-gray-500'}`}>
                {t('customize.step')} 3
              </h3>
              {currentStep >= 3 && (
                <div className="bg-white rounded-xl p-3 space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">📄</span>
                    <span className="font-fredoka text-sm">{selections.pages} {t('customize.pages')}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">🎯</span>
                    <span className="font-fredoka text-sm">{selections.difficulty}</span>
                  </div>
                  {selections.colors.length > 0 && (
                    <div className="flex gap-1">
                      {selections.colors.map((color, i) => (
                        <div key={i} className="w-6 h-6 rounded" style={{ backgroundColor: color }} />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Step 4 */}
            <div className={`p-4 rounded-2xl transition-all ${currentStep === 4 ? 'bg-gradient-magical' : 'bg-gray-200'}`}>
              <h3 className={`text-xl font-fredoka font-bold mb-2 ${currentStep === 4 ? 'text-white' : 'text-gray-500'}`}>
                {t('customize.step')} 4
              </h3>
              {currentStep === 4 && (
                <div className="bg-white rounded-xl p-3">
                  <span className="font-fredoka text-sm">{t('customize.previewPayment')}</span>
                </div>
              )}
            </div>
          </motion.div>

          {/* Mobile Step Indicator */}
          <div className="lg:hidden bg-white/60 backdrop-blur-sm rounded-2xl p-3 mb-4 shadow-lg">
            <div className="flex items-center justify-center gap-2 text-sm font-fredoka">
              <span className={`px-3 py-1 rounded-full ${currentStep === 1 ? 'bg-gradient-magical text-white' : 'bg-gray-200 text-gray-500'}`}>1</span>
              <span className="text-gray-400">→</span>
              <span className={`px-3 py-1 rounded-full ${currentStep === 2 ? 'bg-gradient-magical text-white' : 'bg-gray-200 text-gray-500'}`}>2</span>
              <span className="text-gray-400">→</span>
              <span className={`px-3 py-1 rounded-full ${currentStep === 3 ? 'bg-gradient-magical text-white' : 'bg-gray-200 text-gray-500'}`}>3</span>
              <span className="text-gray-400">→</span>
              <span className={`px-3 py-1 rounded-full ${currentStep === 4 ? 'bg-gradient-magical text-white' : 'bg-gray-200 text-gray-500'}`}>4</span>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 bg-white/70 backdrop-blur-sm rounded-2xl sm:rounded-3xl shadow-xl overflow-hidden">
            <AnimatePresence mode="wait" custom={direction}>
              <motion.div
                key={currentStep}
                custom={direction}
                variants={slideVariants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.5, type: "spring", bounce: 0.2 }}
                className="p-4 sm:p-6 md:p-8 pb-12 sm:pb-16"
              >
                {currentStep === 1 && (
                  <StepOne 
                    selection={selections.theme} 
                    onSelect={(theme) => updateSelection('theme', theme)} 
                  />
                )}
                {currentStep === 2 && (
                  <StepTwo 
                    selection={selections.topic} 
                    onSelect={(topic) => updateSelection('topic', topic)} 
                  />
                )}
                {currentStep === 3 && (
                  <StepThree 
                    selections={selections}
                    onUpdate={updateSelection}
                  />
                )}
                {currentStep === 4 && (
                  <StepFour 
                    selections={selections}
                  />
                )}
              </motion.div>
            </AnimatePresence>

            {/* Navigation Buttons */}
            <div className="flex justify-between p-4 sm:p-6 md:p-8 pt-0 gap-2 sm:gap-4">
              <button
                onClick={handleBack}
                disabled={currentStep === 1}
                className={`px-4 sm:px-6 md:px-8 py-2 sm:py-3 rounded-full font-fredoka font-bold text-base sm:text-lg md:text-xl ${
                  currentStep === 1
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gray-500 text-white hover:bg-gray-600'
                } transition-all`}
              >
                ← {t('customize.back')}
              </button>

              {currentStep < 4 && (
                <button
                  onClick={handleNext}
                  className="px-4 sm:px-6 md:px-8 py-2 sm:py-3 rounded-full font-fredoka font-bold text-base sm:text-lg md:text-xl btn-gradient text-white transition-all"
                >
                  {t('customize.next')} →
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Helper function
const getThemeEmoji = (theme) => {
  const emojis = {
    'Animals': '🦁',
    'Nature': '🌳',
    'Fantasy': '🐉',
    'Science': '🧪',
    'Transport': '🚒',
    'Life': '🌱'
  }
  return emojis[theme] || '✨'
}

export default Customize
