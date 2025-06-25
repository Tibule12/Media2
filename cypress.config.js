const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    specPattern: 'frontend/src/**/*.spec.js',
    supportFile: 'frontend/cypress/support/index.js',
    video: false,
  },
})
