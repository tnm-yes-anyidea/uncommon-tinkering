'''
REQUIREMENTS: speedtest-cli be installed in your system      https://github.com/sivel/speedtest-cli
     CREDIT: 'import json' part was done by Gemini    

     ALSO: change the variable 'filename' to the one where you want to 
        save output

'''


import subprocess
import time
import json
import csv
import os


def run_speedtest():
    try:
        # Running speedtest-cli with JSON output
        result = subprocess.run(['speedtest', '--json'],
                                capture_output=True, text=True)
        data = json.loads(result.stdout)

        # Mbps conversion
        download = round(data['download'] / 1_000_000, 2)
        upload = round(data['upload'] / 1_000_000, 2)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        return [timestamp, download, upload]
    except Exception as e:
        return [time.strftime('%Y-%m-%d %H:%M:%S'), "Error", "Error"]


# Configuration
filename = "speed_results.csv"
interval = 30  # in seconds
duration = 60 * 60  # 1 hour=3600 seconds
end_time = time.time() + duration
all_results = []

# Ensure file has headers if it's new
if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Download (Mbps)", "Upload (Mbps)"])

print(f"Monitoring started. Appending results to {filename}...")

while time.time() < end_time:
    start_loop = time.time()

    # Get stats and update nested list
    stats = run_speedtest()
    all_results.append(stats)

    # Append to CSV file immediately
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(stats)

    print(f"Logged: {stats}")

    # Timing management
    elapsed = time.time() - start_loop
    time.sleep(max(0, interval - elapsed))

print(f"\nDone! Final nested list contains {len(all_results)} entries.")
