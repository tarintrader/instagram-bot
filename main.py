from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

SIMILAR_ACCOUNT = ""
USERNAME = ""
PASSWORD = ""


class InstaFollower:

    def __init__(self):
        self.chrome_options = Options()
        self.prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        self.chrome_options.add_experimental_option("prefs", self.prefs)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument('disable-notifications')
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.implicitly_wait(60)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)
        try:
            self.cookies = self.driver.find_element(By.XPATH,
                                                    value='/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')
            self.cookies.click()
        finally:
            time.sleep(3)
            self.username = self.driver.find_element(By.XPATH,
                                                     value='/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input')
            self.username.send_keys(USERNAME)
            self.password = self.driver.find_element(By.XPATH,
                                                     value='/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input')
            self.password.send_keys(PASSWORD)
            self.login_button = self.driver.find_element(By.XPATH,
                                                         value='/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]')
            self.login_button.click()
            time.sleep(10)

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(10)
        self.followers = self.driver.find_element(By.XPATH,
                                                  value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')
        self.followers.click()
        self.driver.implicitly_wait(10)

        def scroll():
            self.followers_list = self.driver.find_elements(By.XPATH,  '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[*]')
            print(len(self.followers_list))
            self.driver.execute_script("arguments[0].scrollIntoView();", self.followers_list[-1])
            time.sleep(6)
            self.new_followers_list = self.driver.find_elements(By.XPATH,  '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[*]')
            print(len(self.new_followers_list))
            if len(self.new_followers_list) >= 20:
                pass
            elif len(self.new_followers_list) != len(self.followers_list):
                scroll()

        scroll()

    def follow(self):
        self.followers_list = self.driver.find_elements(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[*]//button' )
        [(button.click(), time.sleep(2)) for button in self.followers_list if button.text == "Seguir"]


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
