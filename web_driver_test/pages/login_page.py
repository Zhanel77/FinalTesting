from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_input = (By.ID, "name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.XPATH, "//button[text()='Login']")

    @property
    def username_field(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.name_input))

    @property
    def password_field(self):
        return self.driver.find_element(*self.password_input)

    @property
    def login_button_element(self):
        return self.driver.find_element(*self.login_button)

    def load(self, url):
        self.driver.get(url)

    def login(self, username, password):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.name_input)).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
