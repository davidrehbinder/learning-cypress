// @ts-check
const { test, expect } = require('@playwright/test');

test('has title', async ({ page }) => {
    await page.goto('/');

    // Expect there to be links to 'login' and 'sign up' pages
    await expect(page.getByRole('link', {name: 'Sign in'})).toBeVisible();
    await expect(page.getByRole('link', {name: 'Sign up'})).toBeVisible();

    // Expect login status to not be shown
    await expect(page.locator('#login-status')).toBeHidden();
});