# /// script
# dependencies = [
#   "yt-dlp",
# ]
# ///

"""
How to run it? if you have uv then in CLI 
uv run Download.py
"""

import queue
import threading
import tkinter as tk
from tkinter import ttk

import yt_dlp


class MiniYtQueue:
    def __init__(self, root):
        self.root = root
        self.root.title("YT-DLP Queue")
        self.root.geometry("300x270")  # Increased height for quality dropdown
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.dl_queue = queue.Queue()
        self.is_downloading = False

        self.url_var = tk.StringVar()
        tk.Entry(root, textvariable=self.url_var, width=35).pack(pady=10)

        # Quality selection dropdown
        quality_frame = tk.Frame(root)
        quality_frame.pack(pady=5)
        tk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT, padx=5)
        
        self.quality_var = tk.StringVar(value="720p")
        quality_dropdown = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["720p", "1080p", "Highest"],
            state="readonly",
            width=10
        )
        quality_dropdown.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="MP4", width=8, command=lambda: self.add("mp4")).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="MKV", width=8, command=lambda: self.add("mkv")).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="MP3", width=8, command=lambda: self.add("mp3")).pack(
            side=tk.LEFT, padx=5
        )

        self.listbox = tk.Listbox(root, height=6, width=35, selectbackground="gray")
        self.listbox.pack(pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Idle")
        tk.Label(root, textvariable=self.status_var, fg="blue").pack()

    def add(self, fmt):
        url = self.url_var.get().strip()
        if not url:
            return

        quality = self.quality_var.get()
        self.dl_queue.put((url, fmt, quality))
        self.listbox.insert(tk.END, f"[{fmt.upper()}] {url[:20]}... ({quality})")
        self.url_var.set("")

        if not self.is_downloading:
            self.start_worker()

    def start_worker(self):
        self.is_downloading = True
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        while not self.dl_queue.empty():
            url, fmt, quality = self.dl_queue.get()

            self.root.after(0, self.status_var.set, f"Downloading {fmt.upper()} ({quality})...")
            self.root.after(0, lambda: self.listbox.itemconfig(0, {"bg": "lightgray"}))

            opts = self.get_opts(fmt, quality)
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                print(f"Error: {e}")

            self.root.after(0, lambda: self.listbox.delete(0))
            self.dl_queue.task_done()

        self.root.after(0, self.status_var.set, "Idle")
        self.is_downloading = False

    def get_opts(self, fmt, quality):
        base_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "quiet": True,
            "noprogress": True,
        }

        if fmt == "mp3":
            base_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",  # Highest MP3 bitrate
                    }
                ],
            })
        elif fmt == "mkv":
            if quality == "Highest":
                base_opts.update({
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mkv",
                })
            elif quality == "1080p":
                base_opts.update({
                    "format": "bestvideo[height<=1080]+bestaudio/best",
                    "merge_output_format": "mkv",
                })
            else:  # 720p (default)
                base_opts.update({
                    "format": "bestvideo[height<=720]+bestaudio/best",
                    "merge_output_format": "mkv",
                })
        else:  # mp4
            if quality == "Highest":
                base_opts.update({
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                })
            elif quality == "1080p":
                base_opts.update({
                    "format": "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                })
            else:  # 720p (default)
                base_opts.update({
                    "format": "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                })

        return base_opts


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniYtQueue(root)
    root.mainloop()
