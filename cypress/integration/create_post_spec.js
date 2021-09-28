describe('Can we make a post?', () => {

    before('reset and seed database', () => {
        cy.exec('npm run db:reset && npm run db:seed')
    })

    let cookie
    it('makes post?', () => {
        const {username, password, headline, content} = {'username': 'login_test', 'password': 'login', 'headline': 'headline', 'content': 'body'};
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})
        cy.getCookie('sid').should('exist').then((c) => {
            cookie = c
        }).then(() => {
            cy.setCookie('sid', cookie.value)
            cy.setCookie('username', username)
            cy.request({method: 'POST', url: '/create_post.json', body: {
                username,
                headline,
                content,
            }}).then((response) => {
                expect(response.body).to.have.property('post_id')
            })
        })
    })
})
