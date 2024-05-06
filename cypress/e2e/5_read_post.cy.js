describe('Can we read the posts?', () => {

    before('reset and seed database', () => {
        cy.exec('npm run db:reset && npm run db:seed')
    })

    let cookie
    const {username, password} = {'username': 'login', 'password': 'login_test'};
    it('reads posts through the API', () => {
        cy.request('/post.json').then(
            (response) => {
                expect(response.body).to.have.property('status', 'success')
        })
    })

    it('reads posts through the page', () => {
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})
        cy.visit('/posts.html')
        cy.get('.headline').should('contain', 'headline 1')
        cy.get('.author').should('contain', 'Author: login_test')
        cy.get('.content').should('contain', 'body 1')
    })
})
