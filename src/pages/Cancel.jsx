import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import AnimatedBackground from '../components/AnimatedBackground'

const Cancel = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-100 via-orange-100 to-yellow-100 relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10 min-h-screen flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-3xl p-12 shadow-2xl text-center max-w-2xl w-full"
        >
          {/* Sad Icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="text-9xl mb-6"
          >
            😕
          </motion.div>

          {/* Title */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl font-bubblegum text-gray-800 mb-4"
          >
            Payment Cancelled
          </motion.h1>

          {/* Message */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl font-fredoka text-gray-600 mb-6"
          >
            No worries! Your selections are still saved.
          </motion.p>

          {/* Info Box */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="bg-gradient-to-br from-orange-100 to-yellow-100 rounded-2xl p-6 mb-8"
          >
            <div className="text-6xl mb-4">💭</div>
            <p className="text-lg font-fredoka text-gray-700 mb-2">
              Changed your mind?
            </p>
            <p className="text-md font-fredoka text-gray-600">
              You can go back and complete your order anytime!
            </p>
          </motion.div>

          {/* Reassurance */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-4 mb-8"
          >
            <p className="text-md font-fredoka text-blue-700">
              ✅ No charges were made to your account
            </p>
          </motion.div>

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
              onClick={() => navigate('/customize')}
              className="bg-gradient-magical text-white font-fredoka font-bold text-lg px-8 py-4 rounded-full shadow-lg"
            >
              ← Go Back & Try Again
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/')}
              className="bg-white border-4 border-gray-300 text-gray-700 font-fredoka font-bold text-lg px-8 py-4 rounded-full shadow-lg"
            >
              🏠 Back to Home
            </motion.button>
          </motion.div>

          {/* Footer Note */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-sm font-fredoka text-gray-500 mt-8"
          >
            Need help? Contact us at hera.work.noreply@gmail.com 💌
          </motion.p>
        </motion.div>
      </div>
    </div>
  )
}

export default Cancel
