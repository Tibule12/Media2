describe('Functional Tests', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should register a new user and redirect to login', () => {
    // Delete test user if exists to avoid duplicate registration error
    cy.request({
      method: 'DELETE',
      url: '/api/auth/delete_test_user/',
      failOnStatusCode: false,
    }).then(() => {
      cy.visit('/register')
      cy.get('input[placeholder="Username"]').type('testuser')
      cy.get('input[placeholder="Email"]').type('testuser@example.com')
      cy.get('input[placeholder="Password"]').type('Password123!')
      cy.get('input[placeholder="First Name"]').type('Test')
      cy.get('input[placeholder="Last Name"]').type('User')
      cy.get('button[type="submit"]').contains('Register').click()
      cy.url({ timeout: 10000 }).should('include', '/login')
    })
  })

  it('should login with valid credentials and redirect to home', () => {
    cy.request({
      method: 'POST',
      url: '/api/auth/login/',
      body: {
        email: 'testuser@example.com',
        password: 'Password123!'
      }
    }).then((response) => {
      expect(response.status).to.eq(200)
      window.localStorage.setItem('token', response.body.token)
      cy.visit('/')
      cy.url({ timeout: 10000 }).should('eq', Cypress.config().baseUrl + '/')
    })
  })

  it('should navigate to signup and forgot password from login form', () => {
    cy.visit('/login')
    cy.contains('Signup').click()
    cy.url({ timeout: 10000 }).should('include', '/register')
    cy.visit('/login')
    cy.contains('Forgot Password').click()
    cy.url({ timeout: 10000 }).should('include', '/password-reset')
  })

  it('should navigate to login from register form', () => {
    cy.visit('/register')
    cy.contains('Login').click()
    cy.url({ timeout: 10000 }).should('include', '/login')
  })

  it('should update user profile successfully', () => {
    // Login first before visiting profile page
    cy.request({
      method: 'POST',
      url: '/api/auth/login/',
      body: {
        email: 'testuser@example.com',
        password: 'Password123!'
      }
    }).then((response) => {
      expect(response.status).to.eq(200)
      window.localStorage.setItem('token', response.body.token)
      cy.visit('/profile')
      cy.get('input#fullName').clear().type('Test User Updated')
      cy.get('textarea#bio').clear().type('Updated bio')
      cy.get('button[type="submit"]').contains('Save Profile').click()
      cy.contains('Profile updated successfully.').should('be.visible')
    })
  })

    it('should create a new story with media upload', () => {
    // Login first before visiting story create page
    cy.request({
      method: 'POST',
      url: '/api/auth/login/',
      body: {
        email: 'testuser@example.com',
        password: 'Password123!'
      }
    }).then((response) => {
      expect(response.status).to.eq(200)
      window.localStorage.setItem('token', response.body.token)
      cy.visit('/story/create')
      const imagePath = 'ryan-hutton-Jztmx9yqjBw-unsplash.jpg' // Updated to match the provided image file
      cy.get('input#media').attachFile(imagePath)
      cy.get('button[type="submit"]').contains('Post Story').click()
      cy.contains('Story posted successfully.').should('be.visible')
    })
  })
})
