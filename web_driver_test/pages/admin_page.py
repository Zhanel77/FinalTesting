from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.change_products_button = (By.XPATH, "//button[contains(text(), 'Change Products')]")
        self.product_list = (By.ID, "productList")
        self.delete_button = (By.XPATH, "//ul[@id='productList']/li/button[contains(text(), 'Delete')]")


    def click_change_products(self):
        wait = WebDriverWait(self.driver, 10)
        button = wait.until(EC.element_to_be_clickable(self.change_products_button))
        button.click()
    
    
    def delete_first_product(self):
        wait = WebDriverWait(self.driver, 10)
         
        wait.until(EC.presence_of_element_located(self.product_list)) 
        delete_btn = wait.until(EC.element_to_be_clickable(self.delete_button)) 
        delete_btn.click()

    def check_go_back_button_absent(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.go_back_button)
            )
            raise AssertionError("❌ Button 'Go back to dashboard' exists, but it mustn't be!")
        except TimeoutException:
            pass
