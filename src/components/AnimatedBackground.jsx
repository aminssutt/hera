import React from 'react'

const AnimatedBackground = () => {
  return (
    <div className="animated-background">
      <div className="background-pattern">
        {/* Rockets */}
        <svg className="absolute top-10 left-20 w-16 h-16 float-animation" style={{ animationDelay: '0s' }} viewBox="0 0 100 100">
          <path d="M50 10 L60 40 L70 45 L60 50 L50 80 L40 50 L30 45 L40 40 Z" fill="white" stroke="#5EB3E4" strokeWidth="2"/>
          <circle cx="50" cy="30" r="5" fill="#FFE347"/>
          <path d="M45 85 L40 95 L45 90 Z" fill="#FFAA7A"/>
          <path d="M55 85 L60 95 L55 90 Z" fill="#FFAA7A"/>
        </svg>

        <svg className="absolute top-40 right-32 w-16 h-16 float-animation" style={{ animationDelay: '1s' }} viewBox="0 0 100 100">
          <path d="M50 10 L60 40 L70 45 L60 50 L50 80 L40 50 L30 45 L40 40 Z" fill="white" stroke="#E891C8" strokeWidth="2"/>
          <circle cx="50" cy="30" r="5" fill="#7FD687"/>
          <path d="M45 85 L40 95 L45 90 Z" fill="#FFAA7A"/>
          <path d="M55 85 L60 95 L55 90 Z" fill="#FFAA7A"/>
        </svg>

        <svg className="absolute bottom-32 left-40 w-16 h-16 float-animation" style={{ animationDelay: '2s' }} viewBox="0 0 100 100">
          <path d="M50 10 L60 40 L70 45 L60 50 L50 80 L40 50 L30 45 L40 40 Z" fill="white" stroke="#A97DC0" strokeWidth="2"/>
          <circle cx="50" cy="30" r="5" fill="#FFE347"/>
          <path d="M45 85 L40 95 L45 90 Z" fill="#FFAA7A"/>
          <path d="M55 85 L60 95 L55 90 Z" fill="#FFAA7A"/>
        </svg>

        {/* Stars */}
        {[...Array(15)].map((_, i) => (
          <svg
            key={`star-${i}`}
            className="absolute float-animation"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              width: '24px',
              height: '24px',
              animationDelay: `${Math.random() * 3}s`,
              opacity: 0.6
            }}
            viewBox="0 0 24 24"
            fill="white"
            stroke="#FFE347"
            strokeWidth="2"
          >
            <path d="M12 2 L14.5 9.5 L22 12 L14.5 14.5 L12 22 L9.5 14.5 L2 12 L9.5 9.5 Z" />
          </svg>
        ))}

        {/* Planets */}
        <svg className="absolute top-20 right-20 w-20 h-20 rotate-animation" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="25" fill="#E891C8" opacity="0.7"/>
          <ellipse cx="50" cy="50" rx="40" ry="10" fill="none" stroke="#A97DC0" strokeWidth="2"/>
        </svg>

        <svg className="absolute bottom-40 right-60 w-24 h-24 float-animation" style={{ animationDelay: '1.5s' }} viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="20" fill="#7FD687" opacity="0.7"/>
          <circle cx="45" cy="45" r="5" fill="#90EE90" opacity="0.5"/>
          <circle cx="60" cy="55" r="7" fill="#90EE90" opacity="0.5"/>
        </svg>
      </div>
    </div>
  )
}

export default AnimatedBackground
