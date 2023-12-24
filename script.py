from datetime import datetime, timedelta
import re
import glob
import gzip
from collections import Counter

time_now = datetime.now()
time_24hrs_ago = time_now - timedelta(days=1)
failed_attempts = Counter()

failed_ssh_attempt_re = re.compile(r"Failed password for .* from (\S+) port \d+ ssh2")

for filename in glob.glob("/root/uop/log/auth.log*") + glob.glob(
        "/root/uop/log/auth.log*.gz"
):
    if filename.endswith(".gz"):
        open_func = gzip.open
    else:
        open_func = open

    with open_func(filename, "rt") as file:
        for line in file:
            if "Failed password" not in line:
                continue

            month, day, time_of_day, _, _, _, _ = line.split()[:7]
            log_time_str = f"{month} {day} {time_of_day}"
            log_time = datetime.strptime(log_time_str, "%b %d %H:%M:%S")

            log_time = log_time.replace(year=time_now.year)

            if time_24hrs_ago <= log_time <= time_now:
                failed_match = failed_ssh_attempt_re.search(line)
                if failed_match:
                    ip_address = failed_match.group(1)
                    failed_attempts[ip_address] += 1

with open("/tmp/stat.txt", "w") as out_file:
    for ip, count in failed_attempts.most_common():
        out_file.write(f"{ip}: {count}\n")


def build_html():
    with open("/root/uop/www/head", "r") as out_file:
        head_content = out_file.read

    with open("/root/uop/www/tail", "r") as out_file:
        tail_content = out_file.read

    ipAddresses = ""
    for ip, count in failed_attempts.most_common():
        ipAddresses += f"""
            <div class="ip-item">
                <span class="ip-address">{ip}</span>
                <span class="ip-count">{count}</span>
            </div>"""

    full_index_html = head_content + ip_address + tail_content

    with open("/var/www/html/index.html", "w") as index_html:
        index_html.write(full_index_html)


build_html()
