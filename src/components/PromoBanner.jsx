import { motion } from 'framer-motion'

/**
 * PromoBanner renders either the corner promo badge or the price display section.
 * Use variant="badge" for the absolute-positioned corner sticker,
 * and variant="price" (default) for the price block inside the card.
 */
const PromoBanner = ({ promoInfo, variant = 'price' }) => {
  if (variant === 'badge') {
    if (!promoInfo || !promoInfo.is_promo) return null
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.5, rotate: -15 }}
        animate={{ opacity: 1, scale: 1, rotate: 0 }}
        transition={{ type: 'spring', bounce: 0.5 }}
        className="absolute -top-4 -right-4 bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-bold py-2 px-4 rounded-full shadow-lg transform rotate-12 z-10"
      >
        🔥 {promoInfo.remaining_spots}/{promoInfo.promo_limit} LEFT!
      </motion.div>
    )
  }

  // variant === 'price'
  return (
    <div className="mb-6">
      {promoInfo && promoInfo.is_promo ? (
        <div className="flex flex-col items-center gap-2">
          <span className="text-3xl font-fredoka font-bold text-gray-400 line-through">$9.99</span>
          <div className="flex items-center gap-2">
            <span className="text-6xl font-fredoka font-bold text-orange-500">
              ${promoInfo.price.toFixed(2)}
            </span>
            <span className="bg-red-500 text-white text-sm font-bold px-2 py-1 rounded">-80%</span>
          </div>
          <span className="text-sm font-fredoka text-orange-600 font-bold">LAUNCH SPECIAL!</span>
        </div>
      ) : (
        <span className="text-5xl font-fredoka font-bold text-hera-blue">$9.99</span>
      )}
    </div>
  )
}

export default PromoBanner
