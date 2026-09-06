import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        vicePink: {
          DEFAULT: "#D85075",
          dark: "#B8385C",
          light: "#E87896",
          pastel: "#F9E6EB",
        },
        viceCyan: {
          DEFAULT: "#2894A0",
          dark: "#1A737E",
          light: "#52B4BE",
          pastel: "#E2F4F6",
        },
        viceYellow: {
          DEFAULT: "#D8AF44",
          dark: "#B58C25",
          light: "#F5EBC7",
        },
        viceOrange: "#D86B48",
        retroBeige: {
          DEFAULT: "#ECE3D2",
          dark: "#D5C8B2",
          light: "#F7F2E8",
          frame: "#DDD1BC",
        },
        retroPaper: "#F5EFE4",
        retroCard: "#FAF7EE",
        retroBorder: "#1C1917",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        display: ["var(--font-outfit)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "Courier New", "monospace"],
      },
      boxShadow: {
        "retro-sm": "2px 2px 0px 0px #000000",
        "retro": "3px 3px 0px 0px #000000",
        "retro-lg": "5px 5px 0px 0px #000000",
        "retro-xl": "8px 8px 0px 0px #000000",
        "retro-inset": "inset 2px 2px 0px 0px rgba(0, 0, 0, 0.25)",
      },
    },
  },
  plugins: [],
} satisfies Config;
