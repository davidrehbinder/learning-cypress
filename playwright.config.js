// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * @see https://playwright.dev/docs/test-configuration
 */

// export const STORAGE_STATE = path.join(__dirname, 'playwright/.auth/user.json')

module.exports = defineConfig({
  testDir: './playwright/tests/',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:8080',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    screenshot: "only-on-failure",
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'setup',
      testMatch: 'support/*.setup.ts',
      use: {
        storageState: 'playwright/.auth/user.json'
      }
    },
    {
      name: 'chromium',
      testIgnore: 'tests/2_logged_in/*',
      use: {
        ...devices['Desktop Chrome'],
      },
    },

    {
      name: 'firefox',
      testIgnore: 'tests/2_logged_in/*',
      use: {
        ...devices['Desktop Firefox'],
      },
    },

    {
      name: 'webkit',
      testIgnore: 'tests/2_logged_in/*',
      use: {
        ...devices['Desktop Safari'],
      },
    },

    {
      name: 'chromium-loggedin',
      testIgnore: 'tests/1_logged_out/*',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json'
      },
      dependencies: ['setup']
    },

    {
      name: 'firefox-loggedin',
      testIgnore: 'tests/1_logged_out/*',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'playwright/.auth/user.json'
      },
      dependencies: ['setup']
    },

    {
      name: 'webkit-loggedin',
      testIgnore: 'tests/1_logged_out/*',
      use: {
        ...devices['Desktop Safari'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup']
    },

    /* Test against mobile viewports. */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: { ...devices['Desktop Edge'], channel: 'msedge' },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    // },
  ],

  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://127.0.0.1:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});

