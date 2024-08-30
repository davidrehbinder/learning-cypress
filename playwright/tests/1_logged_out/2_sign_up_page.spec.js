// @ts-check
const { test, expect } = require('@playwright/test');


test.describe('signup page tests', () => {
    let page;
    test.beforeAll(async ({ browser }) => {
        const context = await browser.newContext();
        page = await context.newPage();
        await page.goto('/sign_up.html');
    });

    test('has username and password fields', async () => {
        // Expect login status to not be shown
        await expect(page.locator('#login-status')).toBeHidden();

        // Expect there to be username and password labels
        await expect(page.getByLabel('username')).toBeVisible();
        await expect(page.getByLabel('password')).toBeVisible();

        // ...and two fields for the username and password.
        const inputs = page.getByRole('textbox')
        await expect(inputs).toHaveCount(2);
        await expect(page.getByLabel('username')).toBeVisible()
        await expect(page.getByLabel('username')).toBeEmpty();
        await expect(page.getByLabel('username')).toBeEditable();
        await expect(page.getByLabel('password')).toBeVisible();
        await expect(page.getByLabel('password')).toBeEmpty();
        await expect(page.getByLabel('password')).toBeEditable();
    });

    test('throws error if we attempt to sign up with empty fields', async () => {
        // If both fields are empty...    
        await page.locator('#create_user_ok').click();
        await expect(page.locator('#response')).toContainText('Username and password required.')
        
        // ...or either password field...
        await page.getByLabel('username').type('apa');
        await page.locator('#create_user_ok').click();
        await expect(page.locator('#response')).toContainText('Username and password required.')

        // ...or username field are empty.
        await page.getByLabel('password').type('apa');
        await page.locator('#create_user_ok').click();
        await expect(page.locator('#response')).toContainText('Username and password required.')
    });

    test('throws an error when the password is too short', async () => {
        await page.getByLabel('username').type('user');
        await page.getByLabel('password').type('p');
        await page.locator('#create_user_ok').click();
        await expect(page.locator('#response')).toContainText('Password is too short')
    });

    test('and the happy path, which shows the username when succeessful', async () => {
        // Reset the DB. Probably needs a better solution since there
        // are tests running in parallel, so race conditions exist.
        require('child_process').exec('npm run db:reset')

        await page.getByLabel('username').type('user');
        await page.getByLabel('password').type('password');
        await page.locator('#create_user_ok').click();
        await expect(page.locator('#response')).toContainText('User user created.')
    })
});