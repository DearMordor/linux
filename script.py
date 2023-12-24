from datetime import datetime, timedelta
import re
from collections import Counter

# Set the time range from now to 24 hours ago
time_now = datetime.now()
time_24hrs_ago = time_now - timedelta(days=1)
failed_attempts = Counter()

# Regular expression for matching failed SSH attempts and extracting IP
failed_ssh_attempt_re = re.compile(r'Failed password for .* from (\S+) port \d+ ssh2')

# Assume logs are from the current year for simplicity; adjust as needed
current_year = time_now.year

with open('/root/uop/log/auth.log', 'r') as file:
    for line in file:
        if 'Failed password' not in line:
            continue

        month, day, time_of_day, _, _, _, _ = line.split()[:8]
        log_time_str = f"{month} {day} {time_of_day}"
        log_time = datetime.strptime(log_time_str, '%b %d %H:%M:%S')

        log_time = log_time.replace(year=time_now.year)

        if time_24hrs_ago <= log_time <= time_now:
            failed_match = failed_ssh_attempt_re.search(line)
            if failed_match:
                ip_address = failed_match.group(1)
                failed_attempts[ip_address] += 1

# Write the statistics to a file
with open('/tmp/stat.txt', 'w') as out_file:
    for ip, count in failed_attempts.most_common():
        out_file.write(f"{ip}: {count}\n")
