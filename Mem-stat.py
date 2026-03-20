'''
THIS THING ONLY WORKS FOR LINUX-BASED SYSTEMS AND macOS possibly...........
Will try to add functionality for Windows in the future.

This script also includes the memory of dependencies used......
'''

import subprocess
import platform
import re


things = input(
    "Enter the terminal commands of Applications, with blank separating each of them: ").split()

for thing in things:

    # The 'grep -v grep' part ensures we don't count the search itself
    command = f"ps aux | grep {thing} | grep -v grep | awk '{{sum+=$6}} END {{print sum/1024}}'"

    try:
        output = subprocess.check_output(command, shell=True).decode().strip()
        # If awk doesn't find anything, it might return empty or nan
        memory_val = float(output) if output and output != "0" else 0.0

        print(f"--- Stats for: {thing} ---")
        print(f"Memory: {memory_val:.2f} MB")

    except subprocess.CalledProcessError:
        print(f"Error: Could not retrieve data for {thing}")
        
        
        
        
'''
#AI-BASED ANSWER:

import psutil
import time
import os

def get_proc_stats():
    # Get user input
    targets = input("Enter app names (e.g., chrome, python, discord), separated by spaces: ").split()
    
    print(f"\n{'Application':<20} | {'Memory (MB)':<12} | {'CPU (%)':<8} | {'Procs':<6}")
    print("-" * 55)

    for target in targets:
        total_mem = 0
        total_cpu = 0
        count = 0
        
        # We iterate through all running processes
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
            try:
                # Case-insensitive match
                if target.lower() in proc.info['name'].lower():
                    # Initialize CPU tracking for this process
                    # interval=None tells psutil to start the timer
                    proc.cpu_percent(interval=None)
                    
                    # Add memory (RSS is Resident Set Size - actual RAM used)
                    total_mem += proc.info['memory_info'].rss
                    count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # CPU needs a small delay to measure the 'delta' or change in usage
        time.sleep(0.1)

        # Now we grab the actual CPU usage after that tiny delay
        for proc in psutil.process_iter(['name']):
             try:
                if target.lower() in proc.name().lower():
                    total_cpu += proc.cpu_percent(interval=None)
             except (psutil.NoSuchProcess, psutil.AccessDenied):
                 continue

        if count > 0:
            # Conversion formula: MB = Bytes / 1024^2
            # Using LaTeX for the math:
            # $$ \text{MB} = \frac{\text{Bytes}}{1024^2} $$
            mb_usage = total_mem / (1024 * 1024)
            print(f"{target:<20} | {mb_usage:>12.2f} | {total_cpu:>8.1f} | {count:<6}")
        else:
            print(f"{target:<20} | {'Not Found':>12} | {'-':>8} | {'0':<6}")

if __name__ == "__main__":
    get_proc_stats()

'''
