import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#08080C",
        surface: "#0F0F18",
        surfaceHover: "#161626",
        surfaceCard: "#131320",
        borderDark: "rgba(255, 255, 255, 0.08)",
        borderGlow: "rgba(225, 29, 72, 0.3)",
        crimson: {
          DEFAULT: "#E11D48",
          glow: "rgba(225, 29, 72, 0.4)",
          dark: "#9F1239",
        },
        cyber: {
          blue: "#38BDF8",
          purple: "#A855F7",
          emerald: "#10B981",
          amber: "#F59E0B",
        }
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        display: ["var(--font-outfit)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 25px -5px rgba(225, 29, 72, 0.25)",
        glowBlue: "0 0 25px -5px rgba(56, 189, 248, 0.25)",
        glowPurple: "0 0 25px -5px rgba(168, 85, 247, 0.25)",
        card: "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "float": "float 6s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        }
      }
    },
  },
  plugins: [],
} satisfies Config;
