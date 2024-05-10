import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class LinkedInBot():

    def __init__(self, username, password):

        self.driver = webdriver.Chrome()
        self.baseUrl = "https://www.linkedin.com"
        self.loginUrl = self.baseUrl + "/login"
        self.username = username
        self.password = password

    def login(self):
        self.driver.get(self.loginUrl)
        time.sleep(5)
        try:
            WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(
                (By.ID, "username"))).send_keys(self.username)
            self.driver.find_element_by_id("password").send_keys(self.password)
            self.driver.find_element_by_xpath(
                "//button[contains(text(),'Sign in')]").click()
            self.driver.implicitly_wait(3)

        except:
            print("Too fast bruh!")
            self.driver.quit()

    def post_text(self, text_post, github_link):
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "share-box-feed-entry__trigger--v2"))).click()
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ql-editor"))).send_keys(text_post + "\n" + "Github: " + github_link)
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@data-control-name='share.post']"))).click()

        except Exception as err:
            raise err

    def post_with_image(self, text_post, github_link, imagepaths):
        complete_path = "\n".join(imagepaths)

        print(complete_path)
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "share-box-feed-entry__trigger--v2"))).click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@data-control-name='share.select_image']"))).click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.ID, "image-sharing-detour-container__file-input"))).send_keys(complete_path)
            time.sleep(6)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@data-control-name='confirm_selected_photo']"))).click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ql-editor"))).send_keys(text_post + "\n" + "Github: " + github_link)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@data-control-name='share.post']"))).click()

        except Exception as err:
            raise err
