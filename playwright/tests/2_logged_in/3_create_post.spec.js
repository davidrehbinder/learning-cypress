// @ts-check
import { test, expect } from '@playwright/test';

test.describe('create post tests', () => {
    let context;
    let page;
    
    test.beforeAll(async ({ browser }) => {
        require('child_process').exec('npm run db:seed');

        const browserContext = await browser.newContext();
        context = browserContext;
        page = await browserContext.newPage();
    });

    test.beforeEach(async ({ request }) => {
        const loggedIn = await request.post('/login.json', {
            data: {
                username: 'login',
                password: 'login_test'
            }
        });
        let response = await loggedIn.text();
        await expect(response).toEqual( '{"login": "success"}' )
    });

    test.afterAll(async () => {
        require('child_process').exec('npm run db:reset');
    })

    test('create post through the API', async () => {
        const makePost = await page.request.post('/post.json', {
            data: {
                username: 'login',
                headline: 'headline 2',
                content: 'body 2'
            }
        })
        let response = await makePost.text()
        await expect(response).toContain('post_id')
    });

    test('create post from page', async () => {
        await page.goto('loggedin.html');
        await page.getByRole('textbox', { name: 'Headline' }).type('headline 3')
        await page.getByRole('textbox', { name: 'Content' }).type('body 3')
        await page.getByRole('button', {name: 'Ok' }).click()
        await expect(page.getByLabel('content').toContain('Post created successfully, id'))
    })
});