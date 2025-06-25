// Import commands.js using ES2015 syntax:
import 'cypress-file-upload'

// Custom command for login
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login')
  cy.get('input[placeholder="Username"]').type(username)
  cy.get('input[placeholder="Password"]').type(password)
  cy.get('button[type="submit"]').contains('Login').click()
  cy.url().should('eq', Cypress.config().baseUrl + '/')
})
