import os
import time
import socket  
from datetime import datetime
import pyautogui
import dropbox
from PIL import ImageFilter
from config_manager import ConfigManager
from timezone_manager import TimeZoneManager

import os
import sys

# Lock file to prevent multiple instances
lock_file = 'app.lock'

# Check if the lock file exists
if os.path.exists(lock_file):
    print("Another instance of the application is already running.")
    sys.exit(1)

# Create the lock file
with open(lock_file, 'w') as f:
    f.write(str(os.getpid()))

# Make sure to delete the lock file when exiting
def cleanup():
    if os.path.exists(lock_file):
        os.remove(lock_file)
    print("Lock file removed. Exiting.")

# Register cleanup for a safe shutdown
import atexit
atexit.register(cleanup)

tz_manager = TimeZoneManager()

# Function to check internet connection
def is_connected():
    try:
        # Check connection by pinging a reliable DNS 
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

# Queue to hold files that couldn't be uploaded
upload_queue = []

# Function to upload file to Dropbox
def upload_to_dropbox(file_path, access_token, dropbox_path):
    try:
        dbx = dropbox.Dropbox(access_token)
        with open(file_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"Successfully uploaded {file_path} to Dropbox.")
    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API error: {e}")
        print(f"Queuing {file_path} for retry due to an API error.")
        upload_queue.append((file_path, dropbox_path))  # Queue for retry
    except OSError:
        print(f"No internet connection. Queuing {file_path} for retry.")
        upload_queue.append((file_path, dropbox_path))  # Queue for retry

# Retry failed uploads
def retry_failed_uploads(access_token):
    if is_connected() and upload_queue:
        for file_path, dropbox_path in upload_queue[:]:
            try:
                upload_to_dropbox(file_path, access_token, dropbox_path)
                upload_queue.remove((file_path, dropbox_path))  # Remove if successful
            except Exception as e:
                print(f"Failed to retry upload for {file_path}: {e}")

# Function to capture and upload a screenshot
def capture_and_upload_screenshot_to_dropbox(access_token, blurred=False):
    screenshot = pyautogui.screenshot()

    # Optionally blur the screenshot
    if blurred:
        screenshot = screenshot.filter(ImageFilter.GaussianBlur(15))

    # Save the screenshot locally
    timestamp = tz_manager.get_current_time().strftime('%Y%m%d_%H%M%S')
    screenshot_filename = f'screenshot_{timestamp}.png'
    screenshot.save(screenshot_filename)

    # Upload the screenshot to Dropbox
    dropbox_path = f'/screenshots/{screenshot_filename}'
    upload_to_dropbox(screenshot_filename, access_token, dropbox_path)

    # Optionally delete the local file after uploading
    os.remove(screenshot_filename)

# Function to upload the activity log
def upload_activity_log_to_dropbox(access_token, log_file='activity_log.txt'):
    if os.path.exists(log_file):
        timestamp = tz_manager.get_current_time().strftime('%Y%m%d_%H%M%S')
        dropbox_path = f'/activity_logs/activity_log_{timestamp}.txt'
        upload_to_dropbox(log_file, access_token, dropbox_path)

# Main function to handle periodic screenshot capturing and log uploading
def start_screenshot_manager(dropbox_access_token):
    config = ConfigManager()

    try:
        while True:
            # Get the interval and whether to blur the screenshots from the config
            screenshot_interval = config.get_screenshot_interval()
            blur_screenshots = config.get_blur_screenshots()

            # Capture and upload the screenshot
            capture_and_upload_screenshot_to_dropbox(dropbox_access_token, blurred=blur_screenshots)

            # Retry any failed uploads
            retry_failed_uploads(dropbox_access_token)

            # Upload the activity log
            upload_activity_log_to_dropbox(dropbox_access_token)

            # Wait for the next interval
            time.sleep(screenshot_interval * 60)  # Convert minutes to seconds
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    dropbox_access_token = 'DROPBOX_ACCESS_TOKEN'               
    start_screenshot_manager(dropbox_access_token)
