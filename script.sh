#!/bin/bash

remote_user="user"
remote_host="host"
remote_port="8822"
remote_log_path="/var/log/auth.log*"
local_log_path="/root/uop/log"
web_root="/var/www/html"

scp -P $remote_port $remote_user@$remote_host:$remote_log_path $local_log_path

python3 script.py

cp /root/uop/www/styles.css $web_root
