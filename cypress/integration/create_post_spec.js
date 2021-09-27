describe('Can we make a post?', () => {

    before('reset and seed database', () => {
        cy.exec('npm run db:reset && npm run db:seed')
    })

    let cookie
    it('makes post?', () => {
        const {username, password, headline, body} = {'username': 'login_test', 'password': 'login', 'headline': 'headline', 'body': 'body'};
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})
        cy.getCookie('sid').should('exist').then((c) => {
            cookie = c
        }).then(() => {
            cy.log('cookie', cookie.value)
            cy.request({method: 'POST', url: '/create_post.json', body: {
                username,
                headline,
                body,
            }, headers: {
                'sid': cookie.value,
                'username': username
            }})
        })
    })
})
