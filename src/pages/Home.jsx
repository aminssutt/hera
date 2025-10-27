import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { useState, useEffect } from 'react'

const Home = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [promoInfo, setPromoInfo] = useState(null)

  // Fetch promo info on component mount
  useEffect(() => {
    const fetchPromoInfo = async () => {
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
        const response = await fetch(`${backendUrl}/api/current-price`)
        const data = await response.json()
        setPromoInfo(data)
      } catch (err) {
        console.error('Failed to fetch promo info:', err)
      }
    }
    fetchPromoInfo()
  }, [])

  const scrollToSection = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center p-4 sm:p-6 md:p-8 relative">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-4xl w-full px-2"
        >
          {/* Logo/Title */}
          <motion.h1
            className="text-6xl sm:text-7xl md:text-8xl lg:text-9xl font-bubblegum text-gray-700 mb-6 sm:mb-8"
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, type: "spring", bounce: 0.5 }}
          >
            {t('home.title')}
          </motion.h1>

          {/* Description */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="bg-white/80 backdrop-blur-sm rounded-2xl sm:rounded-3xl p-4 sm:p-6 md:p-8 mb-6 sm:mb-8 shadow-xl"
          >
            <p className="text-xl sm:text-2xl md:text-3xl font-fredoka font-medium text-gray-700 mb-3 sm:mb-4 leading-relaxed">
              {t('home.subtitle')}
            </p>
            <p className="text-base sm:text-lg md:text-xl font-fredoka text-gray-600 leading-relaxed">
              {t('home.description')}
            </p>
          </motion.div>

          {/* Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/customize')}
            className="btn-gradient text-white font-fredoka font-bold text-xl sm:text-2xl md:text-3xl px-8 sm:px-10 md:px-12 py-4 sm:py-5 md:py-6 rounded-full shadow-2xl w-full sm:w-auto"
          >
            {t('home.createButton')}
          </motion.button>

          {/* Scroll Down Indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.8 }}
            className="mt-8 sm:mt-12 flex flex-col items-center cursor-pointer"
            onClick={() => scrollToSection('how-it-works')}
          >
            <p className="text-gray-600 font-fredoka text-base sm:text-lg mb-2">
              {t('home.learnMore')}
            </p>
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
              className="text-3xl sm:text-4xl text-hera-purple"
            >
              ⬇️
            </motion.div>
          </motion.div>

          {/* Decorative elements */}
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="absolute top-20 left-20 text-6xl opacity-70"
          >
            🎨
          </motion.div>
          <motion.div
            animate={{ rotate: -360 }}
            transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
            className="absolute bottom-20 right-20 text-6xl opacity-70"
          >
            ✏️
          </motion.div>
          <motion.div
            animate={{ y: [-10, 10, -10] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            className="absolute top-40 right-40 text-5xl opacity-70"
          >
            🌈
          </motion.div>
        </motion.div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="min-h-screen flex items-center justify-center p-4 sm:p-6 md:p-8 py-12 sm:py-16 md:py-20">
        <div className="max-w-6xl w-full">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl sm:text-5xl md:text-6xl font-bubblegum text-gray-700 text-center mb-8 sm:mb-12 md:mb-16"
          >
            {t('home.howItWorks')}
          </motion.h2>

          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="bg-white/80 backdrop-blur-sm rounded-2xl sm:rounded-3xl p-6 sm:p-8 shadow-xl text-center"
            >
              <div className="text-5xl sm:text-6xl md:text-7xl mb-3 sm:mb-4">1️⃣</div>
              <h3 className="text-2xl sm:text-3xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
                {t('home.chooseTheme')}
              </h3>
              <div className="bg-gradient-to-br from-purple-200 to-pink-200 rounded-2xl p-4 sm:p-6 mb-3 sm:mb-4 h-40 sm:h-48 flex items-center justify-center">
                <div className="grid grid-cols-3 gap-2">
                  <div className="text-3xl sm:text-4xl">🦁</div>
                  <div className="text-3xl sm:text-4xl">🌳</div>
                  <div className="text-3xl sm:text-4xl">🐉</div>
                  <div className="text-3xl sm:text-4xl">🧪</div>
                  <div className="text-3xl sm:text-4xl">🚒</div>
                  <div className="text-3xl sm:text-4xl">🌱</div>
                </div>
              </div>
              <p className="text-sm sm:text-base text-gray-600 font-fredoka">
                {t('home.chooseThemeDesc')}
              </p>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="bg-white/80 backdrop-blur-sm rounded-2xl sm:rounded-3xl p-6 sm:p-8 shadow-xl text-center"
            >
              <div className="text-5xl sm:text-6xl md:text-7xl mb-3 sm:mb-4">2️⃣</div>
              <h3 className="text-2xl sm:text-3xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
                {t('home.customizeStyle')}
              </h3>
              <div className="bg-gradient-to-br from-blue-200 to-cyan-200 rounded-2xl p-4 sm:p-6 mb-3 sm:mb-4 h-40 sm:h-48 flex items-center justify-center">
                <div className="space-y-1 sm:space-y-2 text-left">
                  <div className="font-fredoka text-base sm:text-lg">🎨 Ghibli</div>
                  <div className="font-fredoka text-base sm:text-lg">😄 Cartoon</div>
                  <div className="font-fredoka text-base sm:text-lg">💥 Comic</div>
                  <div className="font-fredoka text-base sm:text-lg">⭕ Minimal</div>
                  <div className="font-fredoka text-base sm:text-lg">✨ Magical</div>
                </div>
              </div>
              <p className="text-sm sm:text-base text-gray-600 font-fredoka">
                {t('home.customizeStyleDesc')}
              </p>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="bg-white/80 backdrop-blur-sm rounded-2xl sm:rounded-3xl p-6 sm:p-8 shadow-xl text-center sm:col-span-2 md:col-span-1"
            >
              <div className="text-5xl sm:text-6xl md:text-7xl mb-3 sm:mb-4">3️⃣</div>
              <h3 className="text-2xl sm:text-3xl font-fredoka font-bold text-gray-700 mb-3 sm:mb-4">
                {t('home.aiGeneration')}
              </h3>
              <div className="bg-gradient-to-br from-green-200 to-yellow-200 rounded-2xl p-4 sm:p-6 mb-3 sm:mb-4 h-40 sm:h-48 flex flex-col items-center justify-center">
                <div className="text-4xl sm:text-5xl mb-2">📚</div>
                <div className="font-fredoka text-base sm:text-lg">10-30 Pages</div>
                <div className="font-fredoka text-base sm:text-lg">Easy/Medium/Hard</div>
                <div className="flex gap-2 mt-2">
                  <div className="w-5 h-5 sm:w-6 sm:h-6 bg-red-400 rounded"></div>
                  <div className="w-5 h-5 sm:w-6 sm:h-6 bg-blue-400 rounded"></div>
                  <div className="w-5 h-5 sm:w-6 sm:h-6 bg-green-400 rounded"></div>
                  <div className="w-5 h-5 sm:w-6 sm:h-6 bg-yellow-400 rounded"></div>
                </div>
              </div>
              <p className="text-sm sm:text-base text-gray-600 font-fredoka">
                {t('home.aiGenerationDesc')}
              </p>
            </motion.div>
          </div>

          {/* Preview Example */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
            className="mt-16 bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-xl"
          >
            <h3 className="text-4xl font-bubblegum text-gray-700 text-center mb-8">
              ✨ {t('home.instantDownload')} ✨
            </h3>
            
            {/* Image Showcase */}
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              {/* Before & After Comparison */}
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 }}
                className="space-y-4"
              >
                <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-4 overflow-hidden shadow-lg">
                  <p className="text-center font-fredoka font-bold text-gray-700 mb-2">
                    🖍️ Ready to Color
                  </p>
                  <motion.img
                    whileHover={{ scale: 1.05 }}
                    src="/images/blackandwhite.png"
                    alt="Black and white coloring page"
                    className="w-full h-auto rounded-xl shadow-md"
                  />
                </div>
                <div className="bg-gradient-to-br from-blue-100 to-cyan-100 rounded-2xl p-4 overflow-hidden shadow-lg">
                  <p className="text-center font-fredoka font-bold text-gray-700 mb-2">
                    🎨 Colored Example
                  </p>
                  <motion.img
                    whileHover={{ scale: 1.05 }}
                    src="/images/coloredpanel.png"
                    alt="Colored example"
                    className="w-full h-auto rounded-xl shadow-md"
                  />
                </div>
              </motion.div>

              {/* Generated Examples */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3 }}
                className="space-y-4"
              >
                <div className="bg-gradient-to-br from-yellow-100 to-orange-100 rounded-2xl p-4 overflow-hidden shadow-lg">
                  <p className="text-center font-fredoka font-bold text-gray-700 mb-2">
                    🌟 AI Generated Design
                  </p>
                  <motion.img
                    whileHover={{ scale: 1.05 }}
                    src="/images/generated_20251016_133814.png"
                    alt="AI generated coloring page 1"
                    className="w-full h-auto rounded-xl shadow-md"
                  />
                </div>
                <div className="bg-gradient-to-br from-green-100 to-teal-100 rounded-2xl p-4 overflow-hidden shadow-lg">
                  <p className="text-center font-fredoka font-bold text-gray-700 mb-2">
                    ✨ Unique Every Time
                  </p>
                  <motion.img
                    whileHover={{ scale: 1.05 }}
                    src="/images/generated_20251016_133901.png"
                    alt="AI generated coloring page 2"
                    className="w-full h-auto rounded-xl shadow-md"
                  />
                </div>
              </motion.div>
            </div>

            {/* Feature Cards */}
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-6 text-center">
                <div className="text-6xl mb-4">🖼️</div>
                <h4 className="text-2xl font-fredoka font-bold text-gray-700 mb-2">
                  Unique Designs
                </h4>
                <p className="text-gray-600 font-fredoka">
                  Every coloring book is generated uniquely for your child with AI technology!
                </p>
              </div>
              <div className="bg-gradient-to-br from-blue-100 to-cyan-100 rounded-2xl p-6 text-center">
                <div className="text-6xl mb-4">🎨</div>
                <h4 className="text-2xl font-fredoka font-bold text-gray-700 mb-2">
                  Kid-Friendly
                </h4>
                <p className="text-gray-600 font-fredoka">
                  Safe, age-appropriate content designed specifically for children to enjoy!
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="min-h-screen flex items-center justify-center p-8 py-20">
        <div className="max-w-6xl w-full">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-5xl md:text-6xl font-bubblegum text-gray-700 text-center mb-16"
          >
            {t('home.pricing')}
          </motion.h2>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* PDF Download */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.05 }}
              className="bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-xl text-center border-4 border-transparent hover:border-hera-blue transition-all relative"
            >
              {/* Promo Badge - Top Right Corner */}
              {promoInfo && promoInfo.is_promo && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.5, rotate: -15 }}
                  animate={{ opacity: 1, scale: 1, rotate: 0 }}
                  transition={{ type: "spring", bounce: 0.5 }}
                  className="absolute -top-4 -right-4 bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-bold py-2 px-4 rounded-full shadow-lg transform rotate-12 z-10"
                >
                  🔥 {promoInfo.remaining_spots}/{promoInfo.promo_limit} LEFT!
                </motion.div>
              )}
              
              <div className="text-7xl mb-4">📱</div>
              <h3 className="text-4xl font-bubblegum text-gray-700 mb-4">
                {t('home.digitalBook')}
              </h3>
              <div className="mb-6">
                {promoInfo && promoInfo.is_promo ? (
                  <div className="flex flex-col items-center gap-2">
                    <span className="text-3xl font-fredoka font-bold text-gray-400 line-through">$9.99</span>
                    <div className="flex items-center gap-2">
                      <span className="text-6xl font-fredoka font-bold text-orange-500">${promoInfo.price.toFixed(2)}</span>
                      <span className="bg-red-500 text-white text-sm font-bold px-2 py-1 rounded">-80%</span>
                    </div>
                    <span className="text-sm font-fredoka text-orange-600 font-bold">LAUNCH SPECIAL!</span>
                  </div>
                ) : (
                  <span className="text-5xl font-fredoka font-bold text-hera-blue">$9.99</span>
                )}
              </div>
              <ul className="text-left space-y-3 mb-8">
                <li className="font-fredoka text-gray-700">{t('home.instantPDF')}</li>
                <li className="font-fredoka text-gray-700">{t('home.printAtHome')}</li>
                <li className="font-fredoka text-gray-700">{t('home.highQuality')}</li>
                <li className="font-fredoka text-gray-700">{t('home.ecoFriendly')}</li>
                <li className="font-fredoka text-gray-700">{t('home.saveMoney')}</li>
              </ul>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/customize')}
                className="w-full bg-hera-blue hover:bg-blue-500 text-white font-fredoka font-bold text-xl py-4 rounded-2xl shadow-lg transition-all"
              >
                {t('home.getDigital')}
              </motion.button>
            </motion.div>

            {/* Physical Book - Coming Soon */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-gradient-to-br from-gray-300 to-gray-400 text-white rounded-3xl p-8 shadow-2xl text-center relative overflow-hidden opacity-75"
            >
              <div className="absolute top-4 right-4 bg-yellow-400 text-gray-800 px-4 py-1 rounded-full font-fredoka font-bold text-sm">
                {t('home.comingSoon').toUpperCase()}
              </div>
              <div className="text-7xl mb-4">📚</div>
              <h3 className="text-4xl font-bubblegum mb-4">
                {t('home.physicalBook')}
              </h3>
              <div className="mb-6">
                <span className="text-5xl font-fredoka font-bold">$24.99</span>
              </div>
              <ul className="text-left space-y-3 mb-8 opacity-60">
                <li className="font-fredoka">{t('home.premiumPaper')}</li>
                <li className="font-fredoka">{t('home.professionalBinding')}</li>
                <li className="font-fredoka">{t('home.shippedToDoor')}</li>
                <li className="font-fredoka">{t('home.durable')}</li>
                <li className="font-fredoka">{t('home.perfectGift')}</li>
              </ul>
              <button
                disabled
                className="w-full bg-gray-500 text-white font-fredoka font-bold text-xl py-4 rounded-2xl shadow-lg cursor-not-allowed"
              >
                {t('home.comingSoon')}
              </button>
            </motion.div>
          </div>

          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center text-gray-600 font-fredoka mt-8 text-lg"
          >
            {t('home.securePayment')}
          </motion.p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="min-h-[60vh] flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="text-center max-w-3xl"
        >
          <h2 className="text-5xl md:text-6xl font-bubblegum text-gray-700 mb-6">
            {t('home.readyToCreate')}
          </h2>
          <p className="text-xl md:text-2xl font-fredoka text-gray-600 mb-8">
            {t('home.joinThousands')}
          </p>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/customize')}
            className="btn-gradient text-white font-fredoka font-bold text-3xl px-16 py-6 rounded-full shadow-2xl"
          >
            {t('home.startCreating')}
          </motion.button>
        </motion.div>
      </section>

      {/* Footer with Contact Button */}
      <footer className="bg-white/80 backdrop-blur-sm py-8 border-t-2 border-gray-200">
        <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-gray-600 font-fredoka text-center md:text-left">
            {t('home.footer')}
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/contact')}
            className="bg-gradient-to-r from-purple-500 to-pink-500 text-white font-fredoka font-bold px-6 py-3 rounded-full shadow-lg hover:shadow-xl transition-all"
          >
            {t('home.shareFeedback')}
          </motion.button>
        </div>
      </footer>
    </div>
  )
}

export default Home
