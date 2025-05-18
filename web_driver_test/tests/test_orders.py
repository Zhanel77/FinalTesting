import sys
import os
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.admin_page import AdminPage
from pages.login_page import LoginPage
from pages.orders_page import OrdersPage
from utils.driver_setup import setup_driver

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.json')
with open(data_path, 'r') as f:
    test_data = json.load(f)

username = test_data['user']['username']
password = test_data['user']['password']
quantity = test_data['order']['quantity']

def test_add_order():
    driver = setup_driver()
    driver.implicitly_wait(5)

    try:
        print("Initializing page objects...")
        login_page = LoginPage(driver)
        orders_page = OrdersPage(driver)
        admin_page = AdminPage(driver)

        fluent_wait = WebDriverWait(
            driver,
            timeout=30,
            poll_frequency=2,
            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]
        )

        wait = WebDriverWait(driver, 10)

        # --- Login ---
        print("Opening login page...")
        login_page.load("https://nodedatabase.onrender.com/users")

        print("Waiting for login inputs...")
        fluent_wait.until(EC.presence_of_element_located((By.ID, "name")))

        print("Filling login form with ActionChains...")
        actions = ActionChains(driver)
        actions.send_keys_to_element(login_page.username_field, username)
        actions.send_keys_to_element(login_page.password_field, password)
        actions.click(login_page.login_button_element)
        actions.perform()

        print("Waiting for dashboard URL...")
        wait.until(EC.url_contains("/dashboard"))
        print("✅ Login successful!")

        # --- Add Order ---
        time.sleep(2)  # wait UI stabilize

        print("Selecting product...")
        select = Select(orders_page.product_dropdown)
        select.select_by_index(1)


        print("Entering quantity and adding order...")
        actions = ActionChains(driver)
        actions.click(orders_page.quantity_field)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
        actions.send_keys(str(quantity))
        actions.click(orders_page.add_order_button_element)
        actions.perform()

        try:
            alert = fluent_wait.until(EC.alert_is_present())
            print(f"✅ Alert message: {alert.text}")
            alert.accept()
        except:
            print("⚠️ No alert appeared")
        time.sleep(2)
        # --- Verify order added ---
        print("Verifying order in list...")
        if orders_page.is_order_added(f"Quantity: {quantity}"):
            print("✅ Order added and visible.")
        else:
            raise AssertionError("❌ Order not found in the list!")

        # --- Delete Order ---
        print("Deleting the order...")
        orders_page.delete_first_product()
        fluent_wait.until(EC.invisibility_of_element_located(
            (By.XPATH, f"//div[contains(text(), 'Quantity: {quantity}')]")
        ))
        print("✅ Order deleted successfully!")

        # --- Admin operations ---
        print("Opening admin panel...")
        admin_page.click_change_products()
        wait.until(EC.url_contains("/admin-prod"))

        print("Deleting first product in admin...")
        admin_page.delete_first_product()
        print("✅ Product deleted successfully!")

        print("Checking that 'Go back to dashboard' button is present...")
        admin_page.check_go_back_button_present()


    except Exception as e:
        print(f"❌ Test failed: {e}")
        driver.save_screenshot("test_failure.png")
        raise

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_add_order()
