import time
import pickle
import obsws_python as obs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ws = obs.ReqClient(host='192.168.1.92', port=4444)



chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")


driver = webdriver.Chrome(options=chrome_options)

# Open the website
driver.get('https://discord.com/')


# Check if cookies file exists and load cookies if it does
cookie_file = 'discord_cookies.json'


try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    # Set the cookies
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Refresh or navigate to the app page after setting cookies
    driver.get('https://discord.com/app')
except FileNotFoundError:
    driver.get('https://discord.com/login')
    print("Please log in to Discord. Waiting for 30 seconds...")
    time.sleep(15)
    # Save the cookies after logging in
    cookies = driver.get_cookies()
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    print("Cookies saved to cookies.pkl")

print("Starting to check if popout window is detected...")

# Simplifying to just check if the popout window is detected, instead of active
initial_window_count = len(driver.window_handles)


def is_popout_open():
    return len(driver.window_handles) > initial_window_count


def start_recording():
    print("Starting recording...")
    ws.start_record()


def stop_recording():
    ws.stop_record()


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
