module.exports = {
  content: [
      "./templates/**/*.{html, js}",
      "./static/**/*.{html, js}",
  ],
  theme: {
    extend: {
      colors: {
        clifford: '#da373d',
      },
      gridAutoColumns: {
        'auto1fr': 'auto 1fr',
      },
      gridTemplateColumns: {
        'auto1fr': 'auto 1fr',

      }
    },
  },
  plugins: [
    'postcss-import',
    'tailwindcss/nesting',
    'tailwindcss/forms',
    'tailwindcss',
    'autoprefixer',
  ],
}
