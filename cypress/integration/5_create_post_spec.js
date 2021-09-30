describe('Can we make a post?', () => {

    before('reset and seed database', () => {
        cy.exec('npm run db:reset && npm run db:seed')
    })

    let cookie
    const {username, password, headline, content} = {'username': 'login_test', 'password': 'login', 'headline': 'headline 1', 'content': 'body 1'};
    it('makes a post by API', () => {
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})
        cy.getCookie('sid').should('exist').then((c) => {
            cookie = c
        }).then(() => {
            cy.setCookie('sid', cookie.value)
            cy.setCookie('username', username)
            cy.request({method: 'POST', url: '/post.json', body: {
                username,
                headline,
                content,
            }}).then((response) => {
                expect(response.body).to.have.property('post_id')
            })
        })
    })

    it('makes a post through the form', () => {
        cy.request({method: 'POST', url: '/login.json', body: {
            username,
            password,
        }})
        cy.visit('/loggedin.html')
        cy.get('#headline').type('headline 2')
        cy.get('#content').type('body 2')
        cy.get('#post_ok').click()
        cy.get('#response').should('contain', 'Post created successfully')
    })
})
