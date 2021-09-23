describe('Checking logged in status.', () => {

    before('reset and seed database', () => {
        cy.exec('npm run db:reset && npm run db:seed')
    })

    it('gets login cookie', () => {
        const {username, password} = {'username': 'login_test', 'password': 'login'};
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})

        cy.visit('/')
        cy.get('#login-status').should('not.be.empty')
    })

})
