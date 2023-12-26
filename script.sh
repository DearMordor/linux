#!/bin/bash

remote_user="user"
remote_host="host"
remote_port="8822"
remote_log_path="/var/log/auth.log*"
uop_path="/root/uop"
local_log_path="$uop_path/log"
web_root="/var/www/html"

scp -P $remote_port $remote_user@$remote_host:$remote_log_path $local_log_path

if [ $? -ne 0 ]; then
    echo "Error in transferring log files."
    exit 1
fi

python3 "$uop_path/script.py"

if [ $? -ne 0 ]; then
    echo "Error in executing Python script."
    exit 1
fi
