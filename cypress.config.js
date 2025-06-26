const { defineConfig } = require('cypress')
const { viteDevServer } = require('@cypress/vite-dev-server')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    specPattern: 'frontend/cypress/e2e/**/*.spec.js',
    supportFile: 'frontend/cypress/support/index.js',
    video: false,
    setupNodeEvents(on, config) {
      on('dev-server:start', (options) => viteDevServer(options))
      return config
    },
  },
  component: {
    devServer: {
      framework: 'vue',
      bundler: 'vite',
    },
  },
})
