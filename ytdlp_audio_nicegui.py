# -*- coding: utf-8 -*-
"""
YT-DLP Audio Downloader & Extractor (.opus)
GUI Framework: NiceGUI
Customized via YT-DLP Python GUI Builder
"""
import os
import sys
import re
import threading
import asyncio
import subprocess
from datetime import datetime

try:
    from nicegui import ui
except ImportError:
    print("NiceGUI not found! Please run: pip install nicegui yt-dlp")
    sys.exit(1)

# App Configuration
DEFAULT_FORMAT = "opus"
DEFAULT_BITRATE = "192"
DEFAULT_DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

class AudioExtractorApp:
    def __init__(self):
        self.downloading = False
        self.progress_percent = 0.0
        self.status_message = "Ready to convert"
        self.download_speed = "0 KiB/s"
        self.eta = "--:--"
        self.log_content = ""

    def append_log(self, text: str):
        self.log_content += text + "\n"
        if hasattr(self, 'log_area'):
            self.log_area.value = self.log_content
            # Scroll down
            ui.run_javascript(f"document.getElementById('c' + {self.log_area.id}).scrollTop = 999999;")

    def update_progress(self, percent: float, speed: str, eta: str, status: str):
        self.progress_percent = percent / 100.0
        self.progress_bar.value = self.progress_percent
        self.speed_label.set_text(f"Speed: {speed} | ETA: {eta}")
        self.status_label.set_text(status)

    def run_ytdlp(self, url: str, output_dir: str, audio_format: str, bitrate: str):
        self.downloading = True
        self.progress_percent = 0.0
        self.log_content = ""
        self.append_log(f"[*] Starting download of: {url}")
        self.append_log(f"[*] Extraction Directory: {output_dir}")
        self.append_log(f"[*] Target Quality: {audio_format} ({bitrate}kbps)\n")

        # Create output directory if not exists
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            self.append_log(f"[!] Error creating folder: {e}")
            self.downloading = False
            return

        # Template for output filename
        outtmpl = os.path.join(output_dir, '%(title)s.%(ext)s')

        # Build yt-dlp command. Uses yt-dlp binary from system path.
        cmd = [
            'yt-dlp',
            '--no-playlist',
            '--extract-audio',
            '--audio-format', audio_format,
            '--audio-quality', bitrate + 'k',
            '-o', outtmpl,
            '--newline', # Crucial for regex line parsing of progress
        ]

        if "True" == "True":
            cmd.append('--embed-thumbnail')

        cmd.append(url)

        # Regex patterns to parse live progress
        # Example output: [download]  12.4% of 15.22MiB at 4.22MiB/s ETA 00:03
        progress_re = re.compile(r'\[download\]\s+(\d+(?:\.\d+)?)\% of [^\s]+ at ([^\s]+) ETA ([^\s]+)')
        
        try:
            # Hide console window on Windows when starting process
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                startupinfo=startupinfo
            )

            current_title_match = ""
            for line in process.stdout:
                line_str = line.strip()
                if not line_str:
                    continue
                
                # Append to console area
                self.append_log(line_str)

                # Parse percentage progress
                match = progress_re.search(line_str)
                if match:
                    percent = float(match.group(1))
                    speed = match.group(2)
                    eta = match.group(3)
                    self.update_progress(percent, speed, eta, f"Downloading: {percent}%")
                elif "Destination:" in line_str:
                    dest_file = os.path.basename(line_str)
                    self.status_label.set_text(f"Extracting/Writing media file...")
                elif "[ExtractAudio]" in line_str:
                    self.status_label.set_text("Converting to high-quality Opus/audio...")

            process.wait()
            
            if process.returncode == 0:
                self.progress_bar.value = 1.0
                self.speed_label.set_text("Extraction Successful!")
                self.status_label.set_text("Finished! Saved successfully.")
                self.append_log("\n[+] SUCCESS: Audio extracted and converted to Opus/audio format.")
                ui.notify("Audio successfully downloaded!", type="positive")
            else:
                self.status_label.set_text("Error occurred during download")
                self.append_log(f"\n[!] ERROR: yt-dlp exited with return code {process.returncode}")
                ui.notify("Extraction failed! Check terminal log.", type="negative")

        except FileNotFoundError:
            self.append_log("\n[!] FATAL ERROR: 'yt-dlp' was not found in your system PATH.")
            self.append_log("Please install yt-dlp first. Run 'pip install yt-dlp' or place yt-dlp.exe in your script directory.")
            self.status_label.set_text("yt-dlp is missing!")
            ui.notify("yt-dlp executable missing on system path!", type="warning")
        except Exception as e:
            self.append_log(f"\n[!] Exception during execution: {e}")
            self.status_label.set_text("Execution failed")
            ui.notify(f"Error: {e}", type="negative")
        finally:
            self.downloading = False
            self.btn_download.enable()

    def start_download_thread(self):
        url = self.url_input.value.strip()
        out_dir = self.dir_input.value.strip()
        fmt = self.fmt_select.value
        bit = self.bitrate_select.value

        if not url:
            ui.notify("Please enter a valid YouTube Link first!", type="warning")
            return

        self.btn_download.disable()
        self.status_label.set_text("Analyzing and initializing stream...")
        threading.Thread(target=self.run_ytdlp, args=(url, out_dir, fmt, bit), daemon=True).start()

    def main_ui(self):
        # Configure overall layout & page
        ui.query('body').style('background-color: #0f172a; color: #f8fafc;')

        with ui.column().classes('w-full max-w-4xl mx-auto p-6 md:p-8 space-y-6'):
            # Header
            with ui.row().classes('items-center justify-between w-full border-b border-slate-700 pb-4 mb-4'):
                with ui.column():
                    ui.label("YT-DLP High-Quality Audio Extractor").classes('text-2xl font-bold text-emerald-400')
                    ui.label("Powered by Python, NiceGUI & yt-dlp").classes('text-xs text-slate-400')
                ui.badge("Opus Edition", color="emerald").classes('p-2 text-sm')

            # Form elements
            with ui.card().classes('w-full bg-slate-800 border border-slate-700 p-5 rounded-xl'):
                ui.label("Download Configuration").classes('text-lg font-semibold text-slate-200 mb-2')
                
                # YouTube Link
                self.url_input = ui.input(
                    label="Paste YouTube Video URL",
                    placeholder="https://www.youtube.com/watch?v=..."
                ).classes('w-full').props('dark outlined color="emerald"')

                # Download configurations in row
                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-4 mt-4'):
                    # Output path
                    self.dir_input = ui.input(
                        label="Destination Folder", 
                        value=DEFAULT_DOWNLOAD_DIR
                    ).classes('w-full col-span-1 md:col-span-2').props('dark outlined color="emerald"')
                    
                    # Format
                    self.fmt_select = ui.select(
                        options=["opus", "mp3", "m4a", "wav", "flac"],
                        value=DEFAULT_FORMAT,
                        label="Format Option"
                    ).classes('w-full col-span-1').props('dark outlined color="emerald"')

                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 gap-4 mt-2'):
                    # Bitrate selector
                    self.bitrate_select = ui.select(
                        options=["128", "192", "256", "320"],
                        value=DEFAULT_BITRATE,
                        label="Audio Bitrate (kbps)"
                    ).classes('w-full').props('dark outlined color="emerald"')

                    with ui.column().classes('justify-center items-start pl-2'):
                        ui.label("Requirements Checklist:").classes('text-xs text-slate-400 font-bold')
                        ui.label("- pip install nicegui yt-dlp").classes('text-xs text-slate-400')
                        ui.label("- FFmpeg binaries configured on system PATH").classes('text-xs text-slate-400')

            # Download triggers / Progress indicators
            with ui.card().classes('w-full bg-slate-800 border border-slate-700 p-5 rounded-xl space-y-4'):
                with ui.row().classes('w-full justify-between items-center'):
                    self.status_label = ui.label("Ready to convert").classes('text-sm font-medium text-slate-300')
                    self.speed_label = ui.label("Speed: 0 KiB/s | ETA: --:--").classes('text-xs font-mono text-slate-400')

                self.progress_bar = ui.linear_progress(value=0.0, show_value=False).classes('w-full').props('color="emerald"')
                
                # Action Button
                self.btn_download = ui.button(
                    "CONVERT & DOWNLOAD AUDIO",
                    on_click=self.start_download_thread
                ).classes('w-full py-3 h-12 text-sm bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg')

            # Log Area
            with ui.card().classes('w-full bg-slate-900 border border-slate-800 p-4 rounded-xl'):
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label("Active Logs / yt-dlp Console Output").classes('text-xs font-mono text-emerald-400 font-bold')
                    ui.button("Clean Screen", on_click=lambda: self.log_area.set_value("")).classes('text-xs').props('flat dense dark color="slate"')
                
                self.log_area = ui.textarea(
                    value="[info] Initialize GUI output logging...\n"
                ).classes('w-full font-mono text-[11px] h-48 bg-black text-slate-300 border border-slate-800 p-2 rounded').props('dark borderless readonly fill-viewport')

if __name__ in {"__main__", "__mp_main__"}:
    app = AudioExtractorApp()
    app.main_ui()
    ui.run(title="YT-DLP High-Quality Audio Extractor", port=8080, reload=False)
