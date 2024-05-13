describe('Checking log in page.', () => {

    before('reset and seed database', () => {
        cy.exec('npm run db:reset && npm run db:seed')
    })

    it('it successfully loads', () => {
        cy.visit('/login.html')
    })

    it('has username and password fields', () => {
        cy.get('label').should('contain', 'Username').and('contain', 'Password')
    })

    it('does not show logged in status', () => {
        cy.get('#login-status').should('be.empty')
    })

    it('shows an error if you try to log in with empty fields', () => {
        cy.get('#login_ok').click()
        cy.get('#response').should('have.text', 'Username and password required.')
        cy.get('#username').type('apa')
        cy.get('#login_ok').click()
        cy.get('#response').should('have.text', 'Username and password required.')
        cy.get('#password').type('apa')
        cy.get('#login_ok').click()
        cy.get('#response').should('have.text', 'Username and password required.')
    })

    it('shows an error if user or password is wrong or does not exist', () => {
        cy.get('#username').type('apa')
        cy.get('#password').type('apa')
        cy.get('#login_ok').click()
        cy.get('#response').should('have.text', 'Login failed.')
    })

    it('shows a success message if login is successful', () => {
        cy.get('#username').type('login')
        cy.get('#password').type('login_test')
        cy.get('#login_ok').click()
        cy.get('#login-status').should('have.text', 'You are logged in as login')
        cy.get('#logout').should('be.visible')
    })

    it('logs you out if you click "log out"', () => {
        cy.get('#logoutButton').click()
        cy.get('#login-status').should('not.be.visible')
        cy.get('#logout').should('not.be.visible')
    })

    it('gets login cookie and verifies the logged in status', () => {
        const {username, password} = {'username': 'login', 'password': 'login_test'};
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})

        cy.visit('/index.html')
        cy.get('#login-status').should('not.be.empty')
    })
})