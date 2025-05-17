from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

class OrdersPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_select = (By.ID, "productSelect")
        self.quantity_input = (By.ID, "quantity")
        self.add_order_button = (By.XPATH, "//button[text()='Add Order']")
        self.order_list = (By.ID, "orderList")

    def add_order(self, quantity):
        wait = WebDriverWait(self.driver, 10)

        # Select product
        select_elem = wait.until(EC.element_to_be_clickable(self.product_select))
        select = Select(select_elem)
        select.select_by_index(1)

        # Enter quantity
        quantity_input = wait.until(EC.element_to_be_clickable(self.quantity_input))
        time.sleep(3)
        self.driver.execute_script("arguments[0].value = '';", quantity_input)
        quantity_input.send_keys(int(quantity))

        # Click add button
        add_button = wait.until(EC.element_to_be_clickable(self.add_order_button))
        add_button.click()

        # Wait for alert (if any)
        try:
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text
            print(f"[INFO] Alert Text: {alert_text}")
            alert.accept()
            return alert_text
        except Exception as e:
            print("❗ No alert appeared:", e)
            return "No alert appeared"
    
    def is_order_added(self, quantity_text):
        order_list_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.order_list))
        return quantity_text in order_list_elem.text
    
    def delete_first_product(self):
        wait = WebDriverWait(self.driver, 20)

        product_div = wait.until(EC.presence_of_element_located((By.ID, "orderList")))
        delete_button = product_div.find_element(
            By.XPATH, ".//button[contains(text(), 'Delete')]")
        delete_button.click()

        # Confirm if alert appears
        try:
            alert = wait.until(EC.alert_is_present())
            print(f"[INFO] Alert: {alert.text}")
            alert.accept()
        except:
            print("[INFO] No alert appeared")

        # Wait until product disappears (or list refreshes)
        wait.until(EC.staleness_of(product_div))  # Waits until div is removed from DOM
        print("✅ Product deleted and page refreshed.")