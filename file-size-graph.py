import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def select_directory():
    """Opens a dialog to select a directory."""
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a Directory to Scan")
    return folder_path

def scan_directory(base_dir):
    """Scans the directory and records individual files and their sizes."""
    file_data = []

    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        folder_name = "[Root]" if rel_path == "." else rel_path

        for f in files:
            file_path = os.path.join(root, f)
            try:
                if os.path.isfile(file_path):
                    size_mb = os.path.getsize(file_path) / (1024 * 1024) # Convert to MB
                    file_data.append({
                        'Directory': folder_name,
                        'FileName': f,
                        'SizeMB': size_mb
                    })
            except OSError:
                pass # Skip broken symlinks or locked files

    return pd.DataFrame(file_data)

def plot_data(df):
    """Plots a bar chart for file counts and a strip plot for individual file sizes."""
    if df.empty:
        print("No files found in the selected directory.")
        return

    # Calculate aggregate data to find the largest directories
    dir_stats = df.groupby('Directory').agg(
        TotalSize=('SizeMB', 'sum'),
        FileCount=('FileName', 'count')
    ).reset_index()

    # Get the top 20 directories by total size so the graph isn't overcrowded
    top_dirs = dir_stats.sort_values(by='TotalSize', ascending=False).head(20)

    # Filter the main file data to ONLY include files from these top 20 directories
    df_top = df[df['Directory'].isin(top_dirs['Directory'])]

    # Define the order so both graphs align perfectly on the X-axis
    order = top_dirs['Directory'].tolist()

    # Set Seaborn theme
    sns.set_theme(style="whitegrid")
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # --- PRIMARY AXIS: Bar Chart (Number of Files) ---
    sns.barplot(
        data=top_dirs,
        x='Directory',
        y='FileCount',
        color='skyblue',
        alpha=0.6, # Make bars slightly transparent so dots pop out
        ax=ax1,
        order=order
    )
    ax1.set_xlabel('Directories', fontsize=12)
    ax1.set_ylabel('Total Number of Files', color='#2b8cbe', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='#2b8cbe')
    ax1.tick_params(axis='x', rotation=45, labelsize=9)

    # --- SECONDARY AXIS: Strip Plot (Individual File Sizes) ---
    ax2 = ax1.twinx()
    sns.stripplot(
        data=df_top,
        x='Directory',
        y='SizeMB',
        color='crimson',
        alpha=0.7,
        jitter=True, # Adds slight horizontal spread so dots don't overlap entirely
        size=5,      # Size of the dots
        ax=ax2,
        order=order
    )
    ax2.set_ylabel('Individual File Size (MB)', color='crimson', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='crimson')
    ax2.grid(False) # Turn off the second grid to keep it clean

    # Final visual adjustments
    plt.title('File Counts vs. Individual File Sizes by Directory', fontsize=14, pad=15)
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    target_dir = select_directory()

    if target_dir:
        print(f"Scanning: {target_dir}...")
        df_files = scan_directory(target_dir)
        plot_data(df_files)
    else:
        print("No directory selected. Exiting.")
