#!/usr/bin/env python3

import pytest
import requests
import subprocess
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

subprocess.check_call('npm run db:reset', shell=True)
subprocess.check_call('npm run db:seed', shell=True)

class LoggedInPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('http://localhost:8080/index.html')

    def testUnauthenticatedLoggedInPage(self):
        self.driver.get('http://localhost:8080/loggedin.html')

        response = self.driver.find_element(By.TAG_NAME, 'body').text
        assert response == 'Forbidden'

    def testAuthenticatedLoggedInPage(self):
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

        self.driver.get('http://localhost:8080/loggedin.html')

        response = True
        try:
            self.driver.find_element(By.ID, 'login-status')
        except NoSuchElementException:
            response = False

        assert response == True

    def testCreatePostThroughPage(self):
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

        self.driver.get('http://localhost:8080/loggedin.html')

        headline = self.driver.find_element(By.ID, 'headline')
        content = self.driver.find_element(By.ID, 'content')
        make_post = self.driver.find_element(By.ID, 'post_ok')

        headline.clear()
        content.clear()
        headline.send_keys('headline 2')
        content.send_keys('body 2')

        make_post.click()

        response = self.wait.until(EC.text_to_be_present_in_element((By.ID,
            'response'), 'Post created successfully'))

        assert response == True

    def testCreatePostThroughAPI(self):
        header = {'Content-Type': 'application/json'}
        request_data = {'username': 'login', 'password': 'login_test'}
        r = requests.post('http://localhost:8080/login.json', json=request_data, headers=header)

        cookies = r.cookies

        post_body = {'username': 'login', 'headline': 'headline 3', 'content': 'body 3'}

        make_post = requests.post('http://localhost:8080/post.json', json=post_body, headers=header, cookies=cookies)

        assert 'post_id' in make_post.text 

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()