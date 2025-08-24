export default [
  {
    files: ["portfolio/static/portfolio/js/**/*.js"],
    ignores: ["node_modules/**", "staticfiles/**", "**/migrations/**"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        window: "readonly",
        document: "readonly",
        localStorage: "readonly",
        history: "readonly",
        fetch: "readonly",
        URLSearchParams: "readonly",
      }
    },
    rules: {
      "no-unused-vars": ["warn", { "argsIgnorePattern": "^_", "varsIgnorePattern": "^_" }],
      "no-undef": "error",
      "no-console": "off",
      "semi": ["error", "always"],
    }
  }
];