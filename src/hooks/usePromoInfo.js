import { useEffect, useState } from 'react'
import { BACKEND_URL } from '../config/api'

const usePromoInfo = () => {
  const [promoInfo, setPromoInfo] = useState(null)

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/current-price`)
      .then(res => {
        if (!res.ok) throw new Error('Network error')
        return res.json()
      })
      .then(data => setPromoInfo(data))
      .catch(err => console.error('Failed to fetch promo info:', err))
  }, [])

  return promoInfo
}

export default usePromoInfo
