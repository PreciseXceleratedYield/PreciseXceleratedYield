import datetime
import pytz

# Get the current time in UTC
current_time_utc = datetime.datetime.now(pytz.utc)

# Convert the UTC time to IST
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = current_time_utc.astimezone(ist)

# Extract the hour and minute components
current_hour = current_time_ist.hour
current_minute = current_time_ist.minute

# Calculate the decimal time
decimal_time = current_hour + (current_minute / 60)

# Calculate tmechk (remaining time in the day) and ensure it's within the range 15 to 5
tmechk = round(float(min(max(round(24 - decimal_time, 2), 6), 15)), 2)
