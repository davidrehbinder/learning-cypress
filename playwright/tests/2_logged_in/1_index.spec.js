import { test, expect } from '@playwright/test';

test('has header', async ({ page }) => {
  await page.goto('/index.html');
  await expect (page.getByText('are logged in')).toBeVisible();
  await expect (page.getByText('Create a post')).toBeVisible();
  await expect (page.getByText('View posts')).toBeVisible();
});
