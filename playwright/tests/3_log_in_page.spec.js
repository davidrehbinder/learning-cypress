// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('login page tests', () => {
    let page;
    test.beforeAll(async ({ browser }) => {
        const context = await browser.newContext();
        page = await context.newPage();
        await page.goto('/login.html');
        require('child_process').exec('npm run db:reset && npm run db:seed')
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
        await page.locator('#login_ok').click();
        await expect(page.locator('#response')).toContainText('Username and password required.')
        
        // ...or either password field...
        await page.getByLabel('username').type('apa');
        await page.locator('#login_ok').click();
        await expect(page.locator('#response')).toContainText('Username and password required.')

        // ...or username field are empty.
        await page.getByLabel('password').type('apa');
        await page.locator('#login_ok').click();
        await expect(page.locator('#response')).toContainText('Username and password required.')
    });

    test('throws an error if user or password is wrong or does not exist', async () => {
        await page.getByLabel('username').type('apa');
        await page.getByLabel('password').type('apa');
        await page.locator('#login_ok').click();
        await expect(page.locator('#response')).toContainText('Login failed.')
    });

    test('and the happy path, which shows a success message and then logs out', async () => {
        await page.getByLabel('username').type('login');
        await page.getByLabel('password').type('login_test');
        await page.locator('#login_ok').click();
        await expect(page.locator('#login-status')).toContainText('You are logged in as login')
        await page.locator('#logout').click();
        await expect(page.locator('#login-status')).toBeHidden();
        await expect(page.locator('#logout')).toBeHidden();
    })
});