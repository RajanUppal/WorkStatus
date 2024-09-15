import time
import pyautogui
from pynput import mouse, keyboard
from datetime import datetime
import threading
import signal
import sys

class ActivityTracker:
    def __init__(self, log_file='activity_log.txt'):
        self.last_mouse_position = pyautogui.position()
        self.last_activity_time = time.time()
        self.key_press_count = 0
        self.mouse_movement_count = 0
        self.log_file = log_file
        self.running = True  # Flag to control the execution of the script

    def start_tracking(self):
        # Start mouse and keyboard listeners in separate threads
        mouse_listener = mouse.Listener(on_move=self.on_mouse_move, on_click=self.on_mouse_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)

        mouse_thread = threading.Thread(target=mouse_listener.start)
        keyboard_thread = threading.Thread(target=keyboard_listener.start)

        mouse_thread.start()
        keyboard_thread.start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Activity tracking stopped.")
        finally:
            self.running = False
            mouse_listener.stop()
            keyboard_listener.stop()
            mouse_thread.join()
            keyboard_thread.join()

    def on_mouse_move(self, x, y):
        self.mouse_movement_count += 1
        if self.is_genuine_activity(x, y, 'mouse_move'):
            self.log_activity(f"Mouse moved to ({x}, {y})")

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            if self.is_genuine_activity(x, y, 'mouse_click'):
                self.log_activity(f"Mouse clicked at ({x}, {y})")

    def on_key_press(self, key):
        self.key_press_count += 1
        if self.is_genuine_activity(None, None, 'key_press'):
            self.log_activity(f"Key pressed: {key}")

    def is_genuine_activity(self, x, y, activity_type):
        current_time = time.time()

        # detect genuine activity:
        if activity_type == 'mouse_move':
            # Check for irregular mouse movement
            if x is not None and y is not None:
                distance = self.calculate_distance(self.last_mouse_position, (x, y))
                self.last_mouse_position = (x, y)
                
                if distance > 0 and distance < 5:  # Mouse moved too little, could be emulated
                    return False
                if distance > 500:  # Mouse moved too much in a short time, could be emulated
                    return False

        elif activity_type == 'key_press':
            # Check for unnatural keyboard input patterns
            time_since_last_activity = current_time - self.last_activity_time

            if self.key_press_count > 5 and time_since_last_activity < 0.1:  # Too many keys pressed too quickly
                return False

        self.last_activity_time = current_time
        return True

    def calculate_distance(self, start, end):
        return ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5

    def log_activity(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {message}\n"
        with open(self.log_file, 'a') as log:
            log.write(log_message)
        print(log_message)

if __name__ == "__main__":
    tracker = ActivityTracker()

    def signal_handler(sig, frame):
        print("Interrupt received, stopping activity tracker...")
        tracker.running = False

    signal.signal(signal.SIGINT, signal_handler)

    tracker.start_tracking()
