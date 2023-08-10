import time
import json
import obsws_python as obs
from selenium import webdriver
import signal

ws = obs.ReqClient(host='localhost', port=4444)

# Chromium Webdriver

options = webdriver.ChromeOptions()
options.add_argument('--enable-logging')
driver = webdriver.Chrome(options=options)

# Adding cookies to check if previously logged in
driver.get('https://discord.com')
cookie_file = 'discord_cookies.json'

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
    return len(driver.window_handles) > initial_window_count

def start_recording():
    print("Starting recording...")
    ws.start_record()


def stop_recording():
    ws.stop_record()


def gentle_exit(signum, frame):
    print("Exiting...")
    stop_recording()
    # Save cookies
    cookies = driver.get_cookies()
    with open(cookie_file, 'w') as file:
        json.dump(cookies, file)
    print("Cookies saved.")
    driver.quit()
    exit(0)

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
