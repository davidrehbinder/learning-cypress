describe('Checking index page.', () => {

    it('it successfully loads.', () => {
        cy.visit('/index.html')
    })

    it('has links to the login and sign up pages.', () => {
        cy.get('#login').should('contain', 'Sign in').and('have.attr', 'href', '/login.html')
        cy.get('#signup').should('contain', 'Sign up').and('have.attr', 'href', '/sign_up.html')
    })

    it('does not show logged in status', () => {
        cy.get('#login-status').should('be.empty')
    })

})