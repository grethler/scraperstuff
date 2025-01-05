#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Florian Grethler <grethlef@dhbw-loerrach.de>
#          Ronald Wagner <wagnerr@dhbw-loerrach.de>

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


class Browser:
    def __init__(self, logger, settings):
        opts = Options()
        #opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome(
            service=ChromeService(),
            options=opts)
        self.logger = logger
        self.settings = settings

    def login_nzz(self):

        #open URL
        self.browser.get(self.settings["urls"]["NZZ"])

        #focus on login form + login
        self.browser.find_element(By.CLASS_NAME, "fup-login").click()
        sleep(1)
        iframe = self.browser.find_element(By.XPATH, "/html/body/div[3]/div/iframe")
        self.browser.switch_to.frame(iframe)
        path = '//*[@id="autofill-form"]/screen-login/p['
        self.browser.find_element(By.XPATH, path+'3]/input').send_keys(self.settings["email"])
        self.browser.find_element(By.XPATH, path+'4]/input').send_keys(self.settings["password"])
        self.browser.find_element(By.XPATH, path+'6]/button').click()
        self.browser.switch_to.default_content()
        sleep(3)

    def searchTask(self):
        self.browser.find_element(By.CLASS_NAME, "fup-archive-query-input").send_keys("Migration")
        self.browser.find_element(By.CLASS_NAME, "fup-s-date-start").send_keys("01.01.2014")
        self.browser.find_element(By.CLASS_NAME, "fup-s-date-end").send_keys("31.01.2024")
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[1]/div").click()
        sleep(3)

    def articleIteration(self):
        counter = 0
        elements = self.browser.find_elements(By.CLASS_NAME, "fup-archive-result-item-article")
        for i in elements:
            if not counter < 2:
                break
            counter += 1
            action = ActionChains(self.browser)
            action.key_down(Keys.CONTROL).click(i).perform()
            action.key_up(Keys.CONTROL).perform()
            self.switchTabContext()

    def switchTabContext(self):
        0



