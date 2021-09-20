describe('Checking index page.', () => {
    it('successfully loads.', () => {
        cy.visit('/')
    })

    it('has links to the login and sign up pages.', () => {
        cy.visit('/')
        cy.contains('Sign in')
        cy.contains('Sign up')
    })

    it('has a functioning login.', () => {
        cy.visit('/login.html')
        cy.contains('Sign In Here!')
    })
})