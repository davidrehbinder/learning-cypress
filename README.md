# learning-cypress

Just learning cypress stuff.

## What it does

Runs a *very* simple web application (currently with four pages - index, login, sign up, and a page that's only viewable in logged in state), and has a bunch of [Cypress](https://cypress.io/) tests running against it.

## Requirements

* Python3 (I wrote the Python bits in Python 3.7)
* NodeJS (I use Node 14.15) for Cypress -- `npm install cypress` should get it.
* SQLite3

## Running it

* Run `server.py` to start the web application, it'll be running on [localhost port 8080](http://localhost:8080).
* Run `npm run cy:open` to open the test runner, or `npm run cy:run` to run the tests headless. If you, like me, use WSL on Windows you probably need to run these in PowerShell rather than a terminal, at least until WSL2's GUI support gets outside the Windows Insider program (*ie* when we hit Windows 11).
* Run `npm run db:reset` to wipe the SQLite DB clean, and `npm run db:seed` to put a user in there.

## DISCLAIMER

This is very much distributed as-is, and is in **no way, shape, or form suitable as anything other than a minor toybox for local hands-on learning**.
