import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const StepFour = ({ selections }) => {
  const [loading, setLoading] = useState(false)
  const [generatedImage, setGeneratedImage] = useState(null)
  const [error, setError] = useState(null)

  const generatePreview = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          theme: selections.theme,
          topic: selections.topic,
          difficulty: selections.difficulty,
          pages: selections.pages,
          colors: selections.colors
        }),
      })

      const data = await response.json()

      if (data.success) {
        setGeneratedImage(data.image)
      } else {
        setError(data.error || 'Failed to generate image')
      }
    } catch (err) {
      setError('Unable to connect to AI service. Please make sure the backend is running.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-4xl font-fredoka font-bold text-gray-700 mb-4">
          🎨 Preview Your Coloring Book
        </h2>
        <p className="font-fredoka text-gray-600 text-lg">
          Generate a preview page to see what your coloring book will look like!
        </p>
      </div>

      {/* Summary Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-magical text-white rounded-3xl p-6"
      >
        <h3 className="text-2xl font-bubblegum mb-4 text-center">
          📋 Your Book Details
        </h3>
        <div className="grid md:grid-cols-2 gap-4 font-fredoka">
          <div className="bg-white/20 rounded-2xl p-4">
            <span className="text-sm opacity-80">Themes:</span>
            <p className="text-lg font-bold">
              {selections.theme.length > 0 ? selections.theme.join(', ') : 'Not selected'}
            </p>
          </div>
          <div className="bg-white/20 rounded-2xl p-4">
            <span className="text-sm opacity-80">Style:</span>
            <p className="text-lg font-bold">{selections.topic || 'Not selected'}</p>
          </div>
          <div className="bg-white/20 rounded-2xl p-4">
            <span className="text-sm opacity-80">Pages:</span>
            <p className="text-lg font-bold">{selections.pages} pages</p>
          </div>
          <div className="bg-white/20 rounded-2xl p-4">
            <span className="text-sm opacity-80">Difficulty:</span>
            <p className="text-lg font-bold">{selections.difficulty}</p>
          </div>
        </div>
      </motion.div>

      {/* Generate Button or Loading */}
      {!generatedImage && !loading && (
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={generatePreview}
          className="w-full btn-gradient text-white font-fredoka font-bold text-2xl py-6 rounded-3xl shadow-2xl"
        >
          ✨ Generate Preview
        </motion.button>
      )}

      {/* Loading Animation */}
      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="bg-white rounded-3xl p-12 text-center shadow-xl"
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="text-8xl mb-6"
            >
              🎨
            </motion.div>
            <h3 className="text-3xl font-bubblegum text-gray-700 mb-4">
              Creating Your Masterpiece...
            </h3>
            <p className="font-fredoka text-gray-600 text-lg mb-6">
              Our AI is generating a unique coloring page just for you!
            </p>
            <div className="flex justify-center gap-2">
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                className="w-4 h-4 bg-hera-purple rounded-full"
              />
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                className="w-4 h-4 bg-hera-blue rounded-full"
              />
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                className="w-4 h-4 bg-hera-pink rounded-full"
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-100 border-4 border-red-300 rounded-3xl p-6 text-center"
        >
          <div className="text-5xl mb-4">❌</div>
          <h3 className="text-2xl font-fredoka font-bold text-red-700 mb-2">
            Oops! Something went wrong
          </h3>
          <p className="font-fredoka text-red-600 mb-4">{error}</p>
          <button
            onClick={generatePreview}
            className="bg-red-500 hover:bg-red-600 text-white font-fredoka font-bold px-8 py-3 rounded-2xl transition-all"
          >
            Try Again
          </button>
        </motion.div>
      )}

      {/* Generated Image Display */}
      <AnimatePresence>
        {generatedImage && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className="bg-white rounded-3xl p-8 shadow-xl"
          >
            <h3 className="text-3xl font-bubblegum text-gray-700 text-center mb-6">
              🌟 Here's Your Preview!
            </h3>
            
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-4 mb-6">
              <img
                src={generatedImage}
                alt="Generated coloring page preview"
                className="w-full h-auto rounded-xl shadow-lg"
              />
            </div>

            <p className="text-center font-fredoka text-gray-600 mb-6">
              This is just one page! Your full book will have {selections.pages} unique pages like this.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={generatePreview}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 font-fredoka font-bold text-xl py-4 rounded-2xl transition-all"
              >
                🔄 Generate Another
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex-1 btn-gradient text-white font-fredoka font-bold text-xl py-4 rounded-2xl shadow-lg"
              >
                💳 Proceed to Payment
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default StepFour
