import os
import re
import shutil
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

# Common audio extensions to look for
AUDIO_EXTS = {".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".alac", ".aiff", ".m4b"}


class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Batch Converter & Copier")
        self.root.geometry("550x350")
        self.root.resizable(False, False)

        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.m3u_choice = tk.IntVar(value=1)  # 1: Update, 2: Delete

        self.is_processing = False

        self.build_ui()

    def build_ui(self):
        # Source Folder Selection
        src_frame = ttk.Frame(self.root, padding=10)
        src_frame.pack(fill=tk.X)
        ttk.Label(src_frame, text="Source Folder:").pack(anchor=tk.W)
        ttk.Entry(src_frame, textvariable=self.source_dir, state="readonly").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(src_frame, text="Browse", command=self.browse_source).pack(
            side=tk.RIGHT
        )

        # Destination Folder Selection
        dst_frame = ttk.Frame(self.root, padding=10)
        dst_frame.pack(fill=tk.X)
        ttk.Label(dst_frame, text="Destination Folder:").pack(anchor=tk.W)
        ttk.Entry(dst_frame, textvariable=self.dest_dir, state="readonly").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(dst_frame, text="Browse", command=self.browse_dest).pack(
            side=tk.RIGHT
        )

        # M3U Playlist Handling Options
        m3u_frame = ttk.LabelFrame(self.root, text="M3U Playlist Handling", padding=10)
        m3u_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Radiobutton(
            m3u_frame,
            text="Keep and update file extensions to .wav",
            variable=self.m3u_choice,
            value=1,
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            m3u_frame,
            text="Delete / Do not copy .m3u files",
            variable=self.m3u_choice,
            value=2,
        ).pack(anchor=tk.W)

        # Progress and Status
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self.root, textvariable=self.status_var, padding=10).pack(fill=tk.X)

        self.progress = ttk.Progressbar(
            self.root, orient=tk.HORIZONTAL, mode="determinate"
        )
        self.progress.pack(fill=tk.X, padx=10)

        # Start Button
        self.start_btn = ttk.Button(
            self.root, text="Start Processing", command=self.start_processing
        )
        self.start_btn.pack(pady=15)

    def browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_dir.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_dir.set(folder)

    def start_processing(self):
        if not self.source_dir.get() or not self.dest_dir.get():
            messagebox.showwarning(
                "Missing Input", "Please select both source and destination folders."
            )
            return

        if self.source_dir.get() == self.dest_dir.get():
            messagebox.showerror(
                "Error", "Source and Destination folders cannot be the same."
            )
            return

        if self.is_processing:
            return

        self.is_processing = True
        self.start_btn.config(state=tk.DISABLED)

        # Run in separate thread to keep UI unblocked
        threading.Thread(target=self.process_files, daemon=True).start()

    def update_m3u_content(self, content):
        # Regex to match known audio extensions at the end of a line
        exts = "|".join(ext.strip(".") for ext in AUDIO_EXTS)
        pattern = r"\.(" + exts + r")$"
        # Replace matching extensions with .wav, multiline mode ensures $ matches end of each line
        return re.sub(pattern, ".wav", content, flags=re.IGNORECASE | re.MULTILINE)

    def process_files(self):
        src_path = Path(self.source_dir.get())
        dst_path = Path(self.dest_dir.get())

        # First pass: count total files for progress bar
        total_files = sum(len(files) for _, _, files in os.walk(src_path))
        self.progress["maximum"] = total_files
        self.progress["value"] = 0

        processed_count = 0

        for root, dirs, files in os.walk(src_path):
            current_src_dir = Path(root)
            # Calculate relative path to maintain folder structure
            rel_path = current_src_dir.relative_to(src_path)
            current_dst_dir = dst_path / rel_path

            # Create destination directory if it doesn't exist
            current_dst_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                src_file = current_src_dir / file
                file_ext = src_file.suffix.lower()

                self.root.after(0, self.status_var.set, f"Processing: {file}")

                if file_ext in AUDIO_EXTS:
                    # Convert to 16-bit 44.1kHz WAV
                    dst_file = current_dst_dir / (src_file.stem + ".wav")
                    self.convert_audio(src_file, dst_file)

                elif file_ext in {".m3u", ".m3u8"}:
                    if self.m3u_choice.get() == 1:
                        # Update M3U
                        dst_file = current_dst_dir / file
                        self.process_m3u_file(src_file, dst_file)
                    # If choice is 2, do nothing (skip copying)

                else:
                    # Standard copy for other files
                    dst_file = current_dst_dir / file
                    shutil.copy2(src_file, dst_file)

                processed_count += 1
                self.root.after(0, self.update_progress, processed_count)

        self.root.after(0, self.finish_processing)

    def convert_audio(self, src, dst):
        # -y : overwrite output files without asking
        # -c:a pcm_s16le : 16-bit PCM codec
        # -ar 44100 : 44.1 kHz sample rate
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-c:a",
            "pcm_s16le",
            "-ar",
            "44100",
            str(dst),
        ]
        try:
            subprocess.run(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {src}: {e}")

    def process_m3u_file(self, src, dst):
        try:
            with open(src, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            updated_content = self.update_m3u_content(content)

            with open(dst, "w", encoding="utf-8") as f:
                f.write(updated_content)
        except Exception as e:
            print(f"Failed to process m3u {src}: {e}")

    def update_progress(self, value):
        self.progress["value"] = value

    def finish_processing(self):
        self.is_processing = False
        self.start_btn.config(state=tk.NORMAL)
        self.status_var.set("Processing Complete!")
        messagebox.showinfo(
            "Done", "All files have been processed and copied successfully."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
