from datetime import datetime
import pytz
import tzlocal  # New library to get the local timezone

class TimeZoneManager:
    def __init__(self, time_zone=None):
        # Use the system's local time zone if none is provided
        if time_zone:
            self.time_zone = pytz.timezone(time_zone)
        else:
            self.time_zone = self.detect_local_time_zone()

    def detect_local_time_zone(self):
        # Automatically detect and return the system's local time zone using tzlocal
        local_tz = tzlocal.get_localzone()  # This will get the system's local timezone
        return local_tz

    def get_current_time(self):
        # Get the current time in the specified time zone
        return datetime.now(self.time_zone)

    def convert_to_utc(self, local_time):
        
        return local_time.astimezone(pytz.utc)

    def convert_from_utc(self, utc_time):
        
        return utc_time.astimezone(self.time_zone)
