/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    container: {
      center: true,
    },
    extend: {
      colors: {
        green: "#1DB954",
        lime: "#1ED760",
        dark: "#121212",
        darker: "#282828",
        darkest: "#191414",
        lightest: "#B3B3B3",
        snow: "#FFFFFF",
        outer: "#8A8993",
      },
    },
  },
  plugins: [],
};
