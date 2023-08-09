from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


popout = None
# Chromium Webdriver

options = webdriver.ChromeOptions()
options.add_argument('--enable-logging')

driver = webdriver.Chrome( options=options)

# Open the website

driver.get('https://discord.com/login')


print("Please log in to Discord and navigate to a server or chat. Waiting for 30 seconds...")
time.sleep(10)



print("Wait finished. Starting to check if the button was clicked...")


def is_popout():
    # Store the original window handle
    main_window = driver.current_window_handle

    # Check for new windows
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            if driver.current_url == "https://discord.com/popout":
                driver.switch_to.window(main_window)  # Switch back to the original window
                return True

    # Switch back to the original window in case the loop didn't find the popout
    driver.switch_to.window(main_window)
    return False

def start_recording():
    print("Starting recording...")
    # Start recording here


popout_detected = False

while not popout_detected:
    if is_popout():
        print("Popout detected!")
        start_recording()
        popout_detected = True
    time.sleep(5)


# Close the browser
# driver.quit()