/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'fredoka': ['Fredoka', 'sans-serif'],
        'bubblegum': ['Bubblegum Sans', 'cursive'],
      },
      colors: {
        'hera-pink': '#E891C8',
        'hera-purple': '#A97DC0',
        'hera-blue': '#5EB3E4',
        'hera-green': '#7FD687',
        'hera-yellow': '#FFE347',
        'hera-orange': '#FFAA7A',
      },
      backgroundImage: {
        'gradient-magical': 'linear-gradient(135deg, #A97DC0 0%, #5EB3E4 100%)',
      },
    },
  },
  plugins: [],
}
