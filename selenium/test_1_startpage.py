#!/usr/bin/env python3

import unittest
from selenium import webdriver

class StartPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/')

    def test_start_page(self):
        sign_in = self.driver.find_element_by_id('login')
        sign_up = self.driver.find_element_by_id('signup')
        login_status = self.driver.find_element_by_id('login-status')

        assert 'Sign in' in sign_in.text
        assert 'Sign up' in sign_up.text
        assert 'Logged in' not in login_status.text

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()