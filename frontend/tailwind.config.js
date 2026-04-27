/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#000000", // Pure black for main bg
        secondary: "#111111", // Very dark grey for panels
        accent: "#f59e0b", // Keeping amber for subtle highlights
        success: "#10b981",
        background: "#000000", // Pure black for root background
        text: "#f8fafc", // Very light grey for text
        "text-muted": "#737373", // Darker muted text color
        "border-color": "#262626", // Dark border color (neutral-800)
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
