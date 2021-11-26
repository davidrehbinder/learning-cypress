#!/usr/bin/env python3

import pytest
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.headless = True

class StartPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8080/')

    def testStartPage(self):
        sign_in = self.driver.find_element(By.ID, 'login')
        sign_up = self.driver.find_element(By.ID, 'signup')
        login_status = self.driver.find_element(By.ID, 'login-status')

        assert 'Sign in' in sign_in.text
        assert 'Sign up' in sign_up.text
        assert 'Logged in' not in login_status.text

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()