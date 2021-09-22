describe('Checking sign up page.', () => {

    before('reset database', () => {
        cy.exec('npm run db:reset')
    })

    it('it successfully loads', () => {
        cy.visit('/sign_up.html')
    })

    it('has username and password fields', () => {
        cy.get('label').should('contain', 'Username').and('contain', 'Password')
    })

    it('does not show logged in status', () => {
        cy.get('#login-status').should('be.empty')
    })

    it('shows an error if you try to sign up with empty fields', () => {
        cy.get('#create_user_ok').click()
        cy.get('#response').should('have.text', 'Username and password required.')
        cy.get('#username').type('apa')
        cy.get('#create_user_ok').click()
        cy.get('#response').should('have.text', 'Username and password required.')
        cy.get('#password').type('apa')
        cy.get('#create_user_ok').click()
        cy.get('#response').should('have.text', 'Username and password required.')
    })

    it('shows an error when password is too short', () => {
        cy.get('#username').type('user')
        cy.get('#password').type('p')
        cy.get('#create_user_ok').click()
        cy.get('#response').should('include.text', 'Password is too short')
    })

    it('shows the username you created when successful', () => {
        cy.get('#username').type('user')
        cy.get('#password').type('password')
        cy.get('#create_user_ok').click()
        cy.get('#response').should('have.text', 'User user created.')
    })

})