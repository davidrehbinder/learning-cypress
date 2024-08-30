import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ request }) => {
  const login = await request.post('/login.json', {
    data: {
      'username': 'login',
      'password': 'login_test'
    }
  });
  expect(await login.ok()).toBeTruthy();
  console.log(login.text)
  await request.storageState({ path: authFile });
});