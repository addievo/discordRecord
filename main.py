import time
import json

import obsws_python as obs
from selenium import webdriver

ws = obs.ReqClient(host='192.168.1.92', port=4444)

# Chromium Webdriver

options = webdriver.ChromeOptions()
options.add_argument('--enable-logging')

driver = webdriver.Chrome(options=options)

# Adding cookies to check if previously logged in

cookie_file = 'discord_cookies.json'

try:
    with open(cookie_file, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

        # Refresh the page to apply the cookies and navigate to app

        driver.get('https://discord.com/app')

except FileNotFoundError:
    print("No cookies file found. Please log in to Discord and navigate to a server or chat. Waiting for 30 seconds...")
    time.sleep(15)

    print("Wait finished. Saving cookies...")

    cookies = driver.get_cookies()
    with open(cookie_file, 'w') as file:
        json.dump(cookies, file)

    print("Cookies saved.")


# Open the website

driver.get('https://discord.com/login')

print("Please log in to Discord and navigate to a server or chat. Waiting for 30 seconds...")
time.sleep(10)

print("Wait finished. Starting to check if popout window is detected...")

# Simplifying to just check if the popout window is detected, instead of active
initial_window_count = len(driver.window_handles)


def is_popout_open():
    return len(driver.window_handles) > initial_window_count


popout_opened = False

# Wait for the popout to open
while not popout_opened:
    if is_popout_open():
        print("Popout detected!")
        popout_opened = True
    time.sleep(5)


def start_recording():
    print("Starting recording...")
    ws.start_record()


def stop_recording():
    ws.stop_record()


if popout_opened:
    start_recording()
    # Wait for the popout to close
    while is_popout_open():
        time.sleep(5)
    print("Popout closed. Stopping recording...")
    stop_recording()
