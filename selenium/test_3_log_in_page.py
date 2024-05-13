#!/usr/bin/env python3

import pytest
import requests
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

subprocess.check_call('npm run db:reset', shell=True)

class LoginPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('http://localhost:8080/login.html')

    def testLoginPage(self):
        labels = self.driver.find_elements(By.CLASS_NAME, 'label')
        username = labels[0].text
        password = labels[1].text
        cancel = self.driver.find_element(By.ID, 'cancel').text
        login = self.driver.find_element(By.ID, 'login_ok').text
        login_status = self.driver.find_element(By.ID, 'login-status').text

        assert login_status is ''
        assert 'Username' in username
        assert 'Password' in password
        assert 'Cancel' in cancel
        assert 'Ok' in login

    def testLoginPageEmpty(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        login = self.driver.find_element(By.ID, 'login_ok')

        username.clear()
        password.clear()

        login.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'response'), 'Username and password required'))

        assert response == True

    def testLoginPagePasswordEmpty(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        login = self.driver.find_element(By.ID, 'login_ok')

        username.clear()
        password.clear()
        username.send_keys('username')

        login.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'response'), 'Username and password required'))

        assert response == True

    def testLoginPageUsernameEmpty(self):
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        login = self.driver.find_element(By.ID, 'login_ok')

        username.clear()
        password.clear()
        password.send_keys('password')

        login.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'response'), 'Username and password required'))

        assert response == True

    def testLoginPageSuccess(self):
        subprocess.check_call('npm run db:reset', shell=True)
        subprocess.check_call('npm run db:seed', shell=True)

        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        login = self.driver.find_element(By.ID, 'login_ok')

        username.clear()
        password.clear()
        username.send_keys('login')
        password.send_keys('login_test')

        login.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'login-status'), 'You are logged in as login'))

        assert response == True

    def testLogout(self):
        subprocess.check_call('npm run db:seed', shell=True)

        header = {'Content-Type': 'application/json'}
        request_data = {'username': 'login', 'password': 'login_test'}
        r = requests.post('http://localhost:8080/login.json', json=request_data, headers=header)

        all_cookies = r.cookies.get_dict()

        cookies = []
        for k,v in all_cookies.items():
            cookie = {}
            cookie.clear()
            cookie['name'] = k
            cookie['value'] = v
            cookies.append(cookie)

        for i in range(0,len(cookies)):
            self.driver.add_cookie(cookies[i])

        self.driver.get('http://localhost:8080/login.html')

        logout = self.driver.find_element(By.ID, 'logoutButton')

        logout.click()

        response = self.driver.find_element(By.ID, 'logout').text

        assert response == ''

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()