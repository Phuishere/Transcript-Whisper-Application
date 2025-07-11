import datetime

# Get current time
def get_time(tz: int = 7) -> str:
    tz = datetime.timezone(datetime.timedelta(seconds = tz * 3600))
    return datetime.datetime.now(tz = tz)

# Get time delta
def time_delta(seconds):
    return datetime.timedelta(seconds = seconds)