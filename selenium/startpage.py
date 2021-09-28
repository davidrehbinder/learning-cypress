#!/usr/bin/env python3

from selenium import webdriver

driver = webdriver.Chrome()

driver.get('http://localhost:8080/')

sign_in = driver.find_element_by_id('login')
sign_up = driver.find_element_by_id('signup')

assert 'Sign in' in sign_in.text
assert 'Sign up' in sign_up.text

driver.quit()