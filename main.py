import signal
import time
import obsws_python as obs
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

print("Make sure OBS is running and setup with the correct port - 4444 before starting this script.")
ws = obs.ReqClient(host='localhost', port=4444)

# Chromium Webdriver

options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
options.add_argument('--enable-logging')
driver = webdriver.Chrome(options=options)

driver.get('https://discord.com/login')
print("Please login and start a call. Then, open the popout window and wait for the recording to start.")

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
        print("File saved to localuser/Videos")
        print("Either close the browser to gracefully exit, or open another popout to record another call.")
        print("The script runs in the background, so you can continue using your computer while recording.")
        stop_recording()
    time.sleep(10)