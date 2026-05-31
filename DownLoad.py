# /// script
# dependencies = [
#   "yt-dlp",
# ]
# ///


import queue
import threading
import tkinter as tk

import yt_dlp


class MiniYtQueue:
    def __init__(self, root):
        self.root = root
        self.root.title("YT-DLP Queue")
        self.root.geometry("280x220")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.dl_queue = queue.Queue()
        self.is_downloading = False

        self.url_var = tk.StringVar()
        tk.Entry(root, textvariable=self.url_var, width=32).pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="MP4", width=8, command=lambda: self.add("mp4")).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="MP3", width=8, command=lambda: self.add("mp3")).pack(
            side=tk.LEFT, padx=5
        )

        self.listbox = tk.Listbox(root, height=6, width=32, selectbackground="gray")
        self.listbox.pack(pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Idle")
        tk.Label(root, textvariable=self.status_var, fg="blue").pack()

    def add(self, fmt):
        url = self.url_var.get().strip()
        if not url:
            return

        self.dl_queue.put((url, fmt))
        self.listbox.insert(tk.END, f"[{fmt.upper()}] {url[:20]}...")
        self.url_var.set("")

        if not self.is_downloading:
            self.start_worker()

    def start_worker(self):
        self.is_downloading = True
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        while not self.dl_queue.empty():
            url, fmt = self.dl_queue.get()

            self.root.after(0, self.status_var.set, f"Downloading {fmt.upper()}...")
            self.root.after(0, lambda: self.listbox.itemconfig(0, {"bg": "lightgray"}))

            opts = self.get_opts(fmt)
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                print(f"Error: {e}")

            self.root.after(0, lambda: self.listbox.delete(0))
            self.dl_queue.task_done()

        self.root.after(0, self.status_var.set, "Idle")
        self.is_downloading = False

    def get_opts(self, fmt):
        if fmt == "mp3":
            return {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": True,
                "noprogress": True,
            }
        else:
            return {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": True,
                "noprogress": True,
            }


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniYtQueue(root)
    root.mainloop()
