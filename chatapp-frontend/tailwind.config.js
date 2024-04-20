/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {},
  },
    plugins: [],
    darkMode: 'class',
    variants: {
      extend: {
        visibility: ['group-hover'],
      },
    },
}

