import json

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        # Load configuration from a JSON file
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default configuration if config file does not exist
            return {
                "screenshot_interval": 5,  # default to 5 minutes
                "blur_screenshots": False
            }

    def get_screenshot_interval(self):
        return self.config_data.get("screenshot_interval", 5)

    def get_blur_screenshots(self):
        return self.config_data.get("blur_screenshots", False)

    def update_config(self, key, value):
        self.config_data[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f, indent=4)
