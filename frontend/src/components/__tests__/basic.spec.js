describe('Basic UI Tests', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should load the welcome page', () => {
    cy.contains('Tibule Media').should('be.visible')
  })

  it('should navigate to login page', () => {
    cy.contains('Login').click()
    cy.url().should('include', '/login')
    cy.get('input[placeholder="Email"]').should('be.visible')
  })

  it('should navigate to register page', () => {
    cy.visit('/register')
    cy.get('input[placeholder="Username"]').should('be.visible')
  })

  it('should navigate to profile page', () => {
    cy.visit('/profile')
    cy.contains('User Profile', { timeout: 10000 }).should('be.visible')
  })

  it('should navigate to story create page', () => {
    cy.visit('/story/create')
    cy.contains('Create Story', { timeout: 10000 }).should('be.visible')
  })
})
