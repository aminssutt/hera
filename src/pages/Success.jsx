import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import AnimatedBackground from '../components/AnimatedBackground'

const Success = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const sessionId = searchParams.get('session_id')
  const [generationStatus, setGenerationStatus] = useState('checking') // checking, generating, completed, error
  const [pdfFilename, setPdfFilename] = useState(null)
  const [statusMessage, setStatusMessage] = useState(t('success.loading'))
  const [showPdf, setShowPdf] = useState(false)

  useEffect(() => {
    if (!sessionId) {
      setGenerationStatus('error')
      setStatusMessage('No session found')
      return
    }

    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
    
    // Poll for generation status every 3 seconds
    const pollInterval = setInterval(() => {
      fetch(`${backendUrl}/api/generation-status/${sessionId}`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            if (data.status === 'completed') {
              setGenerationStatus('completed')
              setPdfFilename(data.pdf_filename)
              setStatusMessage(data.message)
              clearInterval(pollInterval)
            } else if (data.status === 'generating') {
              setGenerationStatus('generating')
              setStatusMessage(data.message)
            } else {
              setGenerationStatus('queued')
              setStatusMessage(data.message)
            }
          }
        })
        .catch(err => {
          console.error('Error checking generation status:', err)
        })
    }, 3000)

    // Cleanup on unmount
    return () => clearInterval(pollInterval)
  }, [sessionId])

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10 min-h-screen flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-3xl p-12 shadow-2xl text-center max-w-4xl w-full"
        >
          {/* Success Icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="text-9xl mb-6"
          >
            🎉
          </motion.div>

          {/* Title */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl font-bubblegum text-gray-800 mb-4"
          >
            {t('success.title')}
          </motion.h1>

          {/* Message */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl font-fredoka text-gray-600 mb-6"
          >
            {t('success.thankYou')}
          </motion.p>

          {/* Generation Status */}
          <AnimatePresence mode="wait">
            {generationStatus !== 'completed' && (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-6 mb-8"
              >
                <div className="text-6xl mb-4 animate-bounce">
                  {generationStatus === 'generating' ? '🎨' : '📚'}
                </div>
                <p className="text-lg font-fredoka text-gray-700 mb-2">
                  {statusMessage}
                </p>
                
                {/* Loading animation */}
                <div className="flex justify-center gap-2 mt-6">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                    className="w-3 h-3 bg-hera-purple rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                    className="w-3 h-3 bg-hera-blue rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                    className="w-3 h-3 bg-hera-pink rounded-full"
                  />
                </div>
              </motion.div>
            )}

            {generationStatus === 'completed' && pdfFilename && (
              <motion.div
                key="completed"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-8"
              >
                {/* Success message */}
                <div className="bg-green-100 rounded-2xl p-6 mb-6">
                  <div className="text-6xl mb-3">✅</div>
                  <p className="text-lg font-fredoka text-green-700 font-bold">
                    {t('success.bookReady')}
                  </p>
                </div>

                {/* PDF Viewer Toggle */}
                {!showPdf && (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowPdf(true)}
                    className="bg-gradient-magical text-white font-fredoka font-bold text-lg px-8 py-4 rounded-full shadow-lg mb-4"
                  >
                    {t('success.viewBook')}
                  </motion.button>
                )}

                {/* PDF Viewer */}
                <AnimatePresence>
                  {showPdf && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mb-6"
                    >
                      <div className="bg-gray-100 rounded-2xl p-4 mb-4">
                        <iframe
                          src={`${import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'}/api/download-pdf/${pdfFilename}`}
                          className="w-full h-[600px] rounded-xl shadow-inner"
                          title="Your Coloring Book"
                        />
                      </div>
                      
                      <div className="flex gap-4 justify-center">
                        <a
                          href={`${import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'}/api/download-pdf/${pdfFilename}`}
                          download
                          className="bg-hera-purple text-white font-fredoka font-bold text-lg px-6 py-3 rounded-full shadow-lg hover:bg-purple-700 transition"
                        >
                          {t('success.downloadButton')}
                        </a>
                        
                        <button
                          onClick={() => setShowPdf(false)}
                          className="bg-gray-200 text-gray-700 font-fredoka font-bold text-lg px-6 py-3 rounded-full shadow-lg hover:bg-gray-300 transition"
                        >
                          {t('success.hidePreview')}
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Order Details */}
          {sessionId && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="bg-gray-50 rounded-2xl p-4 mb-8"
            >
              <p className="text-sm font-fredoka text-gray-500">
                {t('success.orderId')}: {sessionId.substring(0, 20)}...
              </p>
            </motion.div>
          )}

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/')}
              className="bg-gradient-magical text-white font-fredoka font-bold text-lg px-8 py-4 rounded-full shadow-lg"
            >
              {t('success.backToHome')}
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/customize')}
              className="bg-white border-4 border-hera-purple text-hera-purple font-fredoka font-bold text-lg px-8 py-4 rounded-full shadow-lg"
            >
              {t('success.createAnother')}
            </motion.button>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default Success
