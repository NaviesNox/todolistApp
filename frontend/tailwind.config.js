import forms from '@tailwindcss/forms'

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      boxShadow: {
        glow: '0 0 0 1px rgb(255 255 255 / 0.08), 0 10px 30px rgb(0 0 0 / 0.35)',
      },
    },
  },
  plugins: [forms],
}

