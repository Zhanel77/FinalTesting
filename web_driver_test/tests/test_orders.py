import sys
import os
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Add path to modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.admin_page import AdminPage
from pages.login_page import LoginPage
from pages.orders_page import OrdersPage
from utils.driver_setup import setup_driver

# ✅ Загрузка данных из JSON
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.json')
with open(data_path, 'r') as f:
    test_data = json.load(f)

username = test_data['user']['username']
password = test_data['user']['password']
quantity = test_data['order']['quantity']

def test_add_order():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    try:
        print("Opening login page...")
        login_page = LoginPage(driver)
        orders_page = OrdersPage(driver)
        admin_page = AdminPage(driver)

        login_page.load("https://nodedatabase.onrender.com/users")
        time.sleep(1)

        print("Waiting for login input field...")
        wait.until(EC.presence_of_element_located((By.ID, "name")))
        time.sleep(1)

        print("Entering login credentials...")
        login_page.login(username, password)
        time.sleep(2)

        print("Waiting for dashboard redirect...")
        wait.until(EC.url_contains("/dashboard"))
        print("✅ Login successful!")


        time.sleep(3)
        print("Adding order...")
        alert_text = orders_page.add_order(quantity=quantity)
        print(f"✅ Site message: {alert_text}")
        time.sleep(3)

        print("Waiting for orders list update...")
        success = orders_page.is_order_added(f"Quantity: {quantity}")
        assert success, "❌ Order didn't appear in the list!"
        print("✅ Order successfully added and displayed.")

        time.sleep(2)
        print("Deleting first order:")
        orders_page.delete_first_product()
        print("Deleted successfully!")

        time.sleep(3)
        print("Clicking 'Change Products' button...")
        admin_page.click_change_products()
        print("✅ 'Change Products' button clicked successfully.")

        time.sleep(3)
        print("Deleting first product from the list...")
        admin_page.delete_first_product()
        print("✅ Product deleted.")

        time.sleep(6)
        print("Back to dashboard")
        admin_page.check_go_back_button_absent()

    except Exception as e:
        print("❌ An error occurred:", e)
        driver.save_screenshot("error_screenshot.png")
        raise e

    finally:
        print("Closing browser in 2 seconds...")
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    test_add_order()
