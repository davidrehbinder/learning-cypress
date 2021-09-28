#!/usr/bin/env python3

from selenium import webdriver

driver = webdriver.Chrome()

print(type(driver))

driver.get('http://localhost:8080/')

elem = driver.find_element_by_id('login')
assert 'Sign in' in elem