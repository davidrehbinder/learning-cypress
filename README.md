# learning-cypress

An increasingly inaccurately named repository for my process of learning Cypress/Selenium Webdriver/Playwright stuff.

## What it does

Runs a *very* simple web application (currently with four pages - index, login, sign up, and a page that's only viewable in logged in state where you can post data and view the posted data), and has a bunch of [Cypress](https://cypress.io/) and [Selenium Webdriver](https://www.selenium.dev/documentation/webdriver/) tests running against it. I am currently adding support for [Playwright](https://playwright.dev/) using both JavaScript and Python, and JavaScript versions of the Selenium tests.

### The future

There's the beginnings of a skeleton for [Jest](https://jestjs.io/docs/puppeteer)/[Puppeteer](https://pptr.dev/) too, but I never got anywhere when I tried it last -- I'll have a go at it again after we've reached parity for Playwright.

I also plan to add accessibility testing with [cypress-axe](https://github.com/component-driven/cypress-axe), might happen before or after Playwright parity is reached.

## Requirements

* Python3 (I wrote the Python bits for Python 3.12.3) for Selenium (Python version) and Playwright (Python version).
* NodeJS (I use Node 22.1.0) for Cypress, Playwright (JS version), and Selenium (JS version).
* SQLite3.
* The various browser webdrivers.

## Installing

* `npm install` for the Node/JS parts.
* `pip install pytest pytest-playwright selenium` for the Python parts.
* `playwright install` to install the webdrivers for Playwright (seems like it might not be accessible by Selenium, so also do the next line).
* Links for the webdrivers can be found in the [Selenium documentation](https://www.selenium.dev/selenium/docs/api/py/#drivers).

## Running it

* Run `server.py` to start the web application, it'll be running on [localhost port 8080](http://localhost:8080).
* Run `npm run cy:open` to open the Cypress test runner, or `npm run cy:run` to run the tests headless. If you, like me, use WSL on Windows you probably need to run these in PowerShell rather than a terminal, at least until WSL2's GUI support gets outside the Windows Insider program (*ie* when we hit Windows 11).
* Run `npm run wd:run` to run the webdriver test(s).
* Run `npm run pw:open` to open the Playwright UI mode, or `npm run pw:run` to run them headless. See note about `cy:open` and `cy:run` *re:* GUI support on Windows (though this might have changed?).
* Run `npm run db:reset` to wipe the SQLite DB clean, and `npm run db:seed` to put a user in there.

## DISCLAIMER

This is very much distributed as-is, and is in ***no way, shape, or form suitable as anything other than a minor toybox for local hands-on learning***.
