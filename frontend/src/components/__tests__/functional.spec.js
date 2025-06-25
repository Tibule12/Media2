describe('Functional Tests', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should register a new user and redirect to login', () => {
    cy.visit('/register')
    cy.get('input[placeholder="Username"]').type('testuser')
    cy.get('input[placeholder="Email"]').type('testuser@example.com')
    cy.get('input[placeholder="Password"]').type('Password123!')
    cy.get('input[placeholder="First Name"]').type('Test')
    cy.get('input[placeholder="Last Name"]').type('User')
    cy.get('button[type="submit"]').contains('Register').click()
    cy.wait(1000)
    cy.url().should('include', '/login')
  })

  it('should login with valid credentials and redirect to home', () => {
    cy.visit('/login')
    cy.get('input[placeholder="Email"]').type('testuser')
    cy.get('input[placeholder="Password"]').type('Password123!')
    cy.get('button[type="submit"]').contains('Login').click()
    cy.wait(1000)
    cy.url().should('eq', Cypress.config().baseUrl + '/')
  })

  it('should navigate to signup and forgot password from login form', () => {
    cy.visit('/login')
    cy.contains('Signup').click()
    cy.url().should('include', '/register')
    cy.visit('/login')
    cy.contains('Forgot Password').click()
    cy.url().should('include', '/password-reset')
  })

  it('should navigate to login from register form', () => {
    cy.visit('/register')
    cy.contains('Login').click()
    cy.url().should('include', '/login')
  })

  it('should update user profile successfully', () => {
    // Remove cy.login and manually visit profile page for now
    cy.visit('/profile')
    cy.get('input#fullName').clear().type('Test User Updated')
    cy.get('textarea#bio').clear().type('Updated bio')
    cy.get('button[type="submit"]').contains('Save Profile').click()
    cy.contains('Profile updated successfully.').should('be.visible')
  })

  it('should create a new story with media upload', () => {
    // Remove cy.login and manually visit story create page for now
    cy.visit('/story/create')
    const imagePath = 'images/sample.jpg' // Ensure this file exists in cypress/fixtures/images/
    cy.get('input#media').attachFile(imagePath)
    cy.get('button[type="submit"]').contains('Post Story').click()
    cy.contains('Story posted successfully.').should('be.visible')
  })
})
