/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{html,ts}"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4c43ce',
        secondary: '#6c61ff',
      },
      fontFamily: {
        sans: ['Montserrat', 'Lato', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}