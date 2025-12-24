/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cores Harpia (inspiradas em ave de rapina)
        harpia: {
          blue: '#0066FF',
          yellow: '#FFCC00',
          red: '#EF4444',
          green: '#10B981',
          dark: '#0F172A',
          darker: '#020617',
          gray: '#64748B',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
