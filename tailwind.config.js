/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
    './orders/forms.py'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'hop-green': '#34d399',
        'hop-dark': '#0f172a',
        'hop-emerald': '#10b981',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
      }
    }
  },
  plugins: [],
}
