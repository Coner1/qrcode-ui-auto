#!/bin/bash

# Define the process name to monitor
process_name="python3 -m src.main"
process_home="/home/ubuntu/beauty-code-server/qrcode-ui-auto"
while true; do
  # Check if the process is running
  if pgrep -f "$process_name" > /dev/null; then
    echo "$(date +'%Y-%m-%d %T') Process $process_name is already running."
  else
    echo "$(date +'%Y-%m-%d %T') Process $process_name is not running. Starting it up..."

    # Start the process here (replace with your own command)
    # For example:
    # /path/to/your/process
    cd $process_home
    setsid python3 -m src.main &>> log/console.log 2>&1 &
    echo "$(date +'%Y-%m-%d %T') Process $process_name started"

    # Uncomment the line below if you want to exit the loop after starting the process once
    # break
  fi

  # Delay between checks (in seconds)
  sleep 3
done