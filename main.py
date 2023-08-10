import time
import json
import obsws_python as obs
from selenium import webdriver
import signal
from selenium.common.exceptions import WebDriverException
import os

print("Current Working Directory:", os.getcwd())

ws = obs.ReqClient(host='localhost', port=4444)

# Chromium Webdriver

options = webdriver.ChromeOptions()
options.add_argument('--enable-logging')
driver = webdriver.Chrome(options=options)

# Adding cookies to check if previously logged in
driver.get('https://discord.com')
script_directory = os.path.dirname(os.path.realpath(__file__))
cookie_file = os.path.join(script_directory, 'discord_cookies.json')
try:
    with open(cookie_file, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

        # Refresh the page to apply the cookies and navigate to app

        driver.get('https://discord.com/app')

        # Check if the login was successful; if not, ask the user to login manually
        if "login" in driver.current_url:
            raise FileNotFoundError

except FileNotFoundError:
    print("No cookies file found. Please log in to Discord and navigate to a server or chat. Waiting for 30 seconds...")
    time.sleep(15)

    cookies = driver.get_cookies()
    with open(cookie_file, 'w') as file:
        json.dump(cookies, file)

    print("Cookies saved.")

initial_window_count = len(driver.window_handles)

print("Waiting for window popup to start recording...")

def is_popout_open():
    try:
        return len(driver.window_handles) > 1  # Assuming initial window + popout
    except WebDriverException:
        print("Lost connection to Chrome. Exiting.")
        gentle_exit(None, None)
        return False  # This line won't actually be reached due to gentle_exit, but it's here for clarity.

def start_recording():
    print("Starting recording...")
    ws.start_record()


def stop_recording():
    ws.stop_record()
    cookies = driver.get_cookies()
    with open(cookie_file, 'w') as file:
        json.dump(cookies, file)
    print("Cookies updated.")


def gentle_exit(signum, frame):
    print("Exiting gracefully...")
    try:
        stop_recording()
    except WebDriverException:
        print("Could not save cookies due to lost connection to Chrome.")
    finally:
        driver.quit()
        exit(0)

# Register the gentle_exit function to handle termination signals

signal.signal(signal.SIGTERM, gentle_exit)
signal.signal(signal.SIGINT, gentle_exit)


# Continuously check for popouts
while True:
    if is_popout_open():
        print("Popout detected!")
        start_recording()
        # Wait for the popout to close
        while is_popout_open():
            time.sleep(5)
        print("Popout closed. Stopping recording...")
        stop_recording()
    time.sleep(10)