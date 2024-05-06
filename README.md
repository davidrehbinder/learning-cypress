# learning-cypress

An increasingly inaccurately named repository for my process of learning Cypress/Selenium Webdriver/Playwright stuff.

## What it does

Runs a *very* simple web application (currently with four pages - index, login, sign up, and a page that's only viewable in logged in state where you can post data), and has a bunch of [Cypress](https://cypress.io/) and [Selenium Webdriver](https://www.selenium.dev/documentation/webdriver/) tests running against it. I am currently adding support for [Playwright](https://playwright.dev/). There's the beginnings of a skeleton for [Jest](https://jestjs.io/docs/puppeteer)/[Puppeteer](https://pptr.dev/) too, but I never got anywhere when I tried it last. Will have a go at it again after we've reached parity for Playwright.

## Requirements

* Python3 (I wrote the Python bits for Python 3.12.3)
* NodeJS (I use Node 22.1.0) for Cypress and Playwright -- `npm install cypress` and `npm install playwright` should get them.
* SQLite3
* ChromeDriver

## Running it

* Run `server.py` to start the web application, it'll be running on [localhost port 8080](http://localhost:8080).
* Run `npm run cy:open` to open the test runner, or `npm run cy:run` to run the tests headless. If you, like me, use WSL on Windows you probably need to run these in PowerShell rather than a terminal, at least until WSL2's GUI support gets outside the Windows Insider program (*ie* when we hit Windows 11).
* Run `npm run wd:run` to run the webdriver test(s).
* Run `npm run db:reset` to wipe the SQLite DB clean, and `npm run db:seed` to put a user in there.

## DISCLAIMER

This is very much distributed as-is, and is in **no way, shape, or form suitable as anything other than a minor toybox for local hands-on learning**.
