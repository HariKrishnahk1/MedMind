/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Roboto Mono', 'monospace'],
      },
      colors: {
        background: '#f8fafc', // slate-50
        surface: '#ffffff',
        brand: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        risk: {
          low: '#10b981', // emerald-500
          moderate: '#f59e0b', // amber-500
          high: '#f97316', // orange-500
          critical: '#e11d48', // rose-600
        }
      }
    },
  },
  plugins: [],
}
