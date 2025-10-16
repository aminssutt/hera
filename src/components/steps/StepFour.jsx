import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const StepFour = ({ selections }) => {
  const [loading, setLoading] = useState(false)
  const [generatedImage, setGeneratedImage] = useState(null)
  const [error, setError] = useState(null)
  const [format, setFormat] = useState('pdf') // 'pdf' or 'physical'
  const [bookType, setBookType] = useState('blackwhite') // 'blackwhite' or 'colored'

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

  const getTotalPages = () => {
    // Total pages is always the same as selected
    return selections.pages
  }

  const getBlackWhitePages = () => {
    if (bookType === 'blackwhite') {
      return selections.pages
    } else {
      return Math.floor(selections.pages / 2) // Half are B&W
    }
  }

  const getColoredPages = () => {
    if (bookType === 'blackwhite') {
      return 0
    } else {
      return Math.floor(selections.pages / 2) // Half are colored
    }
  }

  const handlePayment = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/create-checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          format: format,
          bookType: bookType,
          selections: selections
          // No preview image - we'll regenerate all N pages fresh
        }),
      })

      const data = await response.json()

      if (data.success) {
        // Redirect to Stripe Checkout
        window.location.href = data.checkout_url
      } else {
        setError(data.error || 'Failed to create checkout session')
      }
    } catch (err) {
      setError('Unable to connect to payment service. Please try again.')
      console.error('Payment Error:', err)
    }
  }

  const getPrice = () => {
    const basePrice = format === 'pdf' ? 9.99 : 24.99
    return basePrice.toFixed(2)
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="text-center">
        <h2 className="text-2xl sm:text-3xl md:text-4xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
          🎨 Preview & Finalize Your Book
        </h2>
        <p className="font-fredoka text-gray-600 text-base sm:text-lg">
          Generate a preview and choose your book format!
        </p>
      </div>

      {/* Summary Card - Only show if no image generated yet */}
      <AnimatePresence>
        {!generatedImage && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-gradient-magical text-white rounded-2xl sm:rounded-3xl p-4 sm:p-6"
          >
            <h3 className="text-xl sm:text-2xl font-bubblegum mb-3 sm:mb-4 text-center">
              📋 Your Book Details
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 font-fredoka">
              <div className="bg-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                <span className="text-xs sm:text-sm opacity-80">Themes:</span>
                <p className="text-base sm:text-lg font-bold">
                  {selections.theme.length > 0 ? selections.theme.join(', ') : 'Not selected'}
                </p>
              </div>
              <div className="bg-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                <span className="text-xs sm:text-sm opacity-80">Style:</span>
                <p className="text-base sm:text-lg font-bold">{selections.topic || 'Not selected'}</p>
              </div>
              <div className="bg-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                <span className="text-xs sm:text-sm opacity-80">Pages:</span>
                <p className="text-base sm:text-lg font-bold">{selections.pages} pages</p>
              </div>
              <div className="bg-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                <span className="text-xs sm:text-sm opacity-80">Difficulty:</span>
                <p className="text-base sm:text-lg font-bold">{selections.difficulty}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

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
          className="bg-red-100 border-2 sm:border-4 border-red-300 rounded-2xl sm:rounded-3xl p-4 sm:p-6 text-center"
        >
          <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">❌</div>
          <h3 className="text-xl sm:text-2xl font-fredoka font-bold text-red-700 mb-2">
            Oops! Something went wrong
          </h3>
          <p className="font-fredoka text-red-600 mb-3 sm:mb-4 text-sm sm:text-base">{error}</p>
          <button
            onClick={generatePreview}
            className="bg-red-500 hover:bg-red-600 text-white font-fredoka font-bold px-6 sm:px-8 py-2 sm:py-3 rounded-xl sm:rounded-2xl transition-all text-sm sm:text-base"
          >
            Try Again
          </button>
        </motion.div>
      )}

      {/* Generated Image Display with Format Selection */}
      <AnimatePresence>
        {generatedImage && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-4 sm:space-y-6"
          >
            {/* Preview Image - Compact */}
            <div className="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 shadow-xl">
              <h3 className="text-xl sm:text-2xl font-bubblegum text-gray-700 text-center mb-3 sm:mb-4">
                🌟 Preview Sample Page
              </h3>
              
              <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl sm:rounded-2xl p-2 sm:p-3 max-w-md mx-auto">
                <img
                  src={generatedImage}
                  alt="Generated coloring page preview"
                  className="w-full h-auto rounded-lg sm:rounded-xl shadow-lg"
                />
              </div>

              <p className="text-center font-fredoka text-gray-600 mt-3 sm:mt-4 text-xs sm:text-sm">
                This is a preview of your coloring book style!
              </p>
            </div>

            {/* Format Selection */}
            <div className="bg-white rounded-3xl p-6 shadow-xl">
              <h3 className="text-2xl font-bubblegum text-gray-700 mb-4">
                📦 Choose Your Format
              </h3>
              <div className="grid md:grid-cols-2 gap-4 mb-6">
                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={() => setFormat('pdf')}
                  className={`p-6 rounded-2xl font-fredoka font-bold text-xl transition-all ${
                    format === 'pdf'
                      ? 'bg-gradient-magical text-white shadow-lg'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  <div className="text-4xl mb-2">📱</div>
                  <div>Digital PDF</div>
                  <div className="text-3xl mt-2">$9.99</div>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={() => setFormat('physical')}
                  className={`p-6 rounded-2xl font-fredoka font-bold text-xl transition-all ${
                    format === 'physical'
                      ? 'bg-gradient-magical text-white shadow-lg'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  <div className="text-4xl mb-2">📚</div>
                  <div>Physical Book</div>
                  <div className="text-3xl mt-2">$24.99</div>
                </motion.button>
              </div>

              {/* Book Type Selection */}
              <h3 className="text-2xl font-bubblegum text-gray-700 mb-4">
                🎨 Choose Your Book Type
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={() => setBookType('blackwhite')}
                  className={`p-6 rounded-2xl font-fredoka transition-all ${
                    bookType === 'blackwhite'
                      ? 'bg-gray-800 text-white shadow-lg ring-4 ring-gray-500'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  <div className="text-4xl mb-2">⚫⚪</div>
                  <div className="font-bold text-lg mb-2">Black & White Only</div>
                  <div className="text-sm opacity-80">
                    {selections.pages} coloring pages to color yourself
                  </div>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={() => setBookType('colored')}
                  className={`p-6 rounded-2xl font-fredoka transition-all ${
                    bookType === 'colored'
                      ? 'bg-gradient-to-br from-pink-400 via-purple-400 to-blue-400 text-white shadow-lg ring-4 ring-purple-300'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  <div className="text-4xl mb-2">🌈</div>
                  <div className="font-bold text-lg mb-2">Colored Version</div>
                  <div className="text-sm opacity-80">
                    {getBlackWhitePages()} B&W + {getColoredPages()} colored ({selections.pages} total)
                  </div>
                </motion.button>
              </div>
            </div>

            {/* Explanation Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-blue-50 border-4 border-blue-200 rounded-3xl p-6"
            >
              <div className="flex items-start gap-4">
                <div className="text-4xl">ℹ️</div>
                <div className="flex-1 font-fredoka">
                  <h4 className="text-xl font-bold text-blue-800 mb-2">
                    {bookType === 'blackwhite' ? 'Black & White Edition' : 'Colored Edition'}
                  </h4>
                  {bookType === 'blackwhite' ? (
                    <p className="text-blue-700">
                      Your book will contain <strong>{selections.pages} unique coloring pages</strong> in black and white,
                      ready for your child to color with their favorite crayons or markers!
                    </p>
                  ) : (
                    <p className="text-blue-700">
                      Your book will contain <strong>{selections.pages} total pages</strong>:
                      <br />• <strong>{getBlackWhitePages()} black & white pages</strong> to color
                      <br />• <strong>{getColoredPages()} colored example pages</strong> using your chosen color palette as inspiration!
                    </p>
                  )}
                </div>
              </div>
            </motion.div>

            {/* Final Summary & Payment */}
            <div className="bg-gradient-magical text-white rounded-3xl p-8 text-center">
              <h3 className="text-3xl font-bubblegum mb-4">
                🎉 Ready to Create Your Book!
              </h3>
              <div className="text-xl font-fredoka mb-2">
                <strong>{format === 'pdf' ? 'Digital PDF' : 'Physical Book'}</strong> • 
                <strong> {bookType === 'blackwhite' ? ' Black & White' : ' Colored Edition'}</strong>
              </div>
              <div className="text-lg font-fredoka mb-6 opacity-90">
                {bookType === 'colored' ? (
                  <>{getBlackWhitePages()} B&W + {getColoredPages()} Colored = {getTotalPages()} pages</>
                ) : (
                  <>{getTotalPages()} pages</>
                )} • {selections.difficulty} difficulty
              </div>
              <div className="text-5xl font-bold mb-6">
                ${getPrice()}
              </div>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handlePayment}
                className="bg-white text-hera-purple font-fredoka font-bold text-2xl px-12 py-5 rounded-full shadow-2xl hover:shadow-3xl transition-all"
              >
                💳 Proceed to Payment
              </motion.button>
              
              <p className="text-sm mt-4 opacity-75">
                🔒 Secure payment with Stripe • Payment coming soon!
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default StepFour
