# Discord Meeting Recorder

This script automates the process of recording Discord call popouts using OBS (Open Broadcaster Software) and Selenium with Python.

## Prerequisites

1. **Python**: Ensure you have Python installed on your system. If not, download and install it from [Python's official website](https://www.python.org/downloads/).
2. **OBS**: Ensure OBS is installed and set up on your system. Download it from [OBS's official website](https://obsproject.com/).
3. **Python Libraries**: You'll need some Python libraries. Install them using pip:

   ```
   pip install obsws-python selenium
   ```

4. **Webdriver**: This script uses Selenium with Chrome. Ensure you have the [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) downloaded and placed in a location in your system's PATH. 

## Highly recommended to directly install Chrome on your system to prevent reliance on chromedriver.

## Dependencies can be installed by using the requirements.txt

```bash
cd dir_to_proj
pip install -r requirements.txt
```

## Usage

1. **Start OBS**: Before running the script, ensure OBS is running and set up with the correct port, which is 4444 by default.
2. **Run the script**: Navigate to the directory containing the script and run:

   ```
   python main.py
   ```

3. The script will open a Chrome window navigating to Discord's login page.
4. **Login to Discord**: Manually log in to Discord in the opened Chrome window.
5. **Start a Call**: Begin a call on Discord and open it in a popout window.
6. The script will detect the popout window and start recording the call in OBS.
7. Once the popout window is closed, the recording will stop, and the video will be saved to your default OBS recording location (usually `Videos` folder in your user directory).

## Features

- The script can detect multiple popouts, meaning after one call is recorded and closed, you can start another call, and the script will continue recording.
- You can close the main Chrome window (the one showing Discord's main interface) without affecting the recording. Only closing the popout will stop the recording.
- If you want to gracefully exit the script, close the browser window. The script will save the recording and exit.

## Notes

- Ensure that OBS is correctly set up to record the screen or window where the Discord popout will appear.
- The script runs in the background, allowing you to use your computer while recording.

## Output

The application will save recorded files in Videos folder in the current users directory.

## About the Author

Aditya Varma is a computer science graduate from the University of Wollongong. He has a keen interest in AI, cybersecurity, systems analysis, and web development.

## Disclaimer

Always inform participants in a call if you are recording. Recording without consent may be illegal in some jurisdictions.

## Created for [Matrix.ai](https://matrix.ai/)
