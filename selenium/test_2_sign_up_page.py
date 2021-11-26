#!/usr/bin/env python3

import pytest
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.headless = True

subprocess.check_call('npm run db:reset', shell=True)

class SignUpPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('http://localhost:8080/sign_up.html')

    def testSignUpPage(self):
        labels = self.driver.find_elements(By.CLASS_NAME, 'label')
        username = labels[0].text
        password = labels[1].text
        cancel = self.driver.find_element(By.ID, 'cancel').text
        create_user = self.driver.find_element(By.ID, 'create_user_ok').text
        login_status = self.driver.find_element(By.ID, 'login-status').text

        assert login_status is ''
        assert 'Username' in username
        assert 'Password' in password
        assert 'Cancel' in cancel
        assert 'Ok' in create_user

    def testSignUpPageEmpty(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        create_user = self.driver.find_element(By.ID, 'create_user_ok')

        username.clear()
        password.clear()

        create_user.click()

        response = self.driver.find_element(By.ID, 'response').text

        assert 'Username and password required' in response

    def testSignUpPagePasswordEmpty(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        create_user = self.driver.find_element(By.ID, 'create_user_ok')

        username.clear()
        password.clear()
        username.send_keys('username')

        create_user.click()

        response = self.driver.find_element(By.ID, 'response').text

        assert 'Username and password required' in response

    def testSignUpPageUsernameEmpty(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        create_user = self.driver.find_element(By.ID, 'create_user_ok')

        username.clear()
        password.clear()
        password.send_keys('password')

        create_user.click()

        response = self.driver.find_element(By.ID, 'response').text

        assert 'Username and password required' in response

    def testSignUpPagePasswordTooShort(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        create_user = self.driver.find_element(By.ID, 'create_user_ok')

        username.clear()
        password.clear()
        username.send_keys('user')
        password.send_keys('p')

        create_user.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'response'), 'Password is too short'))

        assert response == True

    def testSignUpPageSuccess(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        create_user = self.driver.find_element(By.ID, 'create_user_ok')

        username.clear()
        password.clear()
        username.send_keys('user')
        password.send_keys('password')

        create_user.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'response'), 'User user created'))

        assert response == True

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()