
# WorkStatus Python Agent

## Overview

WorkStatus is a Python-based desktop agent application designed to track employee activity and upload relevant data (such as screenshots) to cloud storage. It includes features for activity tracking, configurable screenshot intervals, time zone management, data upload, and robust error handling.

## Table of Contents

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)


## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/RajanUppal/workstatus.git
   cd workstatus
   ```

2. **Create and Configure Dropbox App**

   - Go to [Dropbox App Console](https://www.dropbox.com/developers/apps) and create a new app.
   - Generate an access token and add it to your `screenshot_manager.py` file.

## Dependencies

The project uses the following third-party libraries:

- `pyautogui` - For taking screenshots and tracking user input.
- `pynput` - For listening to mouse and keyboard events.
- `dropbox` - For uploading files to Dropbox.
- `Pillow` - For image processing (e.g., blurring screenshots).
- `pytz` - For timezone handling.
- `tzlocal` - For detecting the local timezone.

Install these dependencies in the project.

## Configuration

The application uses a JSON configuration file (`config.json`) to manage settings:

- **`screenshot_interval`**: Interval (in minutes) at which screenshots are taken.
- **`blur_screenshots`**: Boolean to determine if screenshots should be blurred.

To update the configuration, modify `config.json` or use the `ConfigManager` class in `config_manager.py`.

## Running the Application

1. **Ensure Only One Instance is Running**

   The application uses a lock file (`app.lock`) to prevent multiple instances.

2. **Start the Application**

   - `activity_tracker.py` will start tracking user activity.
   - `screenshot_manager.py` will handle screenshot capturing and uploading.

   ```bash
   python src/activity_tracker.py
   python src/screenshot_manager.py
   ```


3. **Stopping the Application**

   You can stop the application gracefully using `Ctrl+C`. It will handle cleanup and exit properly.

