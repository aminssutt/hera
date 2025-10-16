import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import AnimatedBackground from '../components/AnimatedBackground'

const Success = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const sessionId = searchParams.get('session_id')
  const [status, setStatus] = useState('processing')

  useEffect(() => {
    // Optional: Verify payment status with backend
    if (sessionId) {
      fetch(`http://localhost:5000/api/session-status/${sessionId}`)
        .then(res => res.json())
        .then(data => {
          if (data.success && data.status === 'paid') {
            setStatus('success')
          }
        })
        .catch(err => {
          console.error('Error checking payment status:', err)
        })
    }
  }, [sessionId])

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10 min-h-screen flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-3xl p-12 shadow-2xl text-center max-w-2xl w-full"
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
            Payment Successful!
          </motion.h1>

          {/* Message */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl font-fredoka text-gray-600 mb-6"
          >
            Thank you for your order! 🎨
          </motion.p>

          {/* Status */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-6 mb-8"
          >
            <div className="text-6xl mb-4 animate-bounce">📚</div>
            <p className="text-lg font-fredoka text-gray-700 mb-2">
              Your custom coloring book is being generated...
            </p>
            <p className="text-md font-fredoka text-gray-600">
              You'll receive an email with your book shortly!
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

          {/* Order Details */}
          {sessionId && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="bg-gray-50 rounded-2xl p-4 mb-8"
            >
              <p className="text-sm font-fredoka text-gray-500">
                Order ID: {sessionId.substring(0, 20)}...
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
              🏠 Back to Home
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/customize')}
              className="bg-white border-4 border-hera-purple text-hera-purple font-fredoka font-bold text-lg px-8 py-4 rounded-full shadow-lg"
            >
              🎨 Create Another Book
            </motion.button>
          </motion.div>

          {/* Footer Note */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-sm font-fredoka text-gray-500 mt-8"
          >
            Check your email inbox (and spam folder) for your coloring book! 📧
          </motion.p>
        </motion.div>
      </div>
    </div>
  )
}

export default Success
