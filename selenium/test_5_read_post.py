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
subprocess.check_call('npm run db:seed', shell=True)

class PostsPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('http://localhost:8080/index.html')

    def testUnauthenticatedPostsPage(self):
        subprocess.check_call('npm run db:reset', shell=True)

        self.driver.get('http://localhost:8080/posts.html')

        response = self.driver.find_element(By.ID, 'post-list').text
        assert response == ''

    def testAuthenticatedPostsPage(self):
        subprocess.check_call('npm run db:reset', shell=True)
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

        self.driver.get('http://localhost:8080/posts.html')

        response = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME,
            'headline'), 'headline'))

        assert response == True
  
    def testReadPostThroughAPI(self):
        header = {'Content-Type': 'application/json'}
        request_data = {'username': 'login', 'password': 'login_test'}
        r = requests.post('http://localhost:8080/login.json', json=request_data, headers=header)
 
        cookies = r.cookies
 
        get_post = requests.get('http://localhost:8080/post.json', headers=header, cookies=cookies)
 
        assert 'success' in get_post.text 

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()