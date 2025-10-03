/** @type {import('tailwindcss').Config} */
module.exports = {
  // Pull in your preset (colors, spacing, fonts, shadows, etc.)
  presets: [require("./ui.preset.js")],

  // Tell Tailwind where to look for class names in a Django project
  content: [
    "./templates/**/*.html",
    "./blog/templates/**/*.html",
    "./blog/**/*.py",
  ],

  // You can still add project-level tweaks here
  theme: {
    extend: {
      container: { center: true, padding: "1rem" },
    },
  },

  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
  ],
};

