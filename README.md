## 💕Download YouTube audio in Opus format using yt-dlp and Python GUI

A sleek, local, web-based graphical user interface (GUI) for yt-dlp, purpose-built for extracting high-fidelity audio from YouTube videos. Built using Python and NiceGUI, this tool provides an elegant dark-themed dashboard to streamline downloading, format conversion, and automated metadata embedding.

## 💖 Acknowledgments & Credits

This project is a graphical wrapper that relies heavily on the incredible work of the open-source community. Special thanks to:

* **[yt-dlp](https://github.com/yt-dlp/yt-dlp):** The powerhouse command-line audio/video downloader that makes the core functionality of this app possible. 
* **[NiceGUI](https://nicegui.io/):** For providing an amazingly simple, reactive, and beautiful web-UI framework for Python.
* **[Mutagen](https://github.com/quodlibet/mutagen):** For handling the audio metadata and artwork tagging seamlessly.



##📸 Screenshots

![Opus Downloadr](/assets/YT-DLP-gui.png)

✨ Features

1. Modern Web-Based UI: Clean, responsive, and distraction-free dark interface powered by NiceGUI.

2. High-Fidelity Audio: Fully optimized for extracting native high-quality audio formats like Opus.

3. Automated Post-Processing:

4. Automatically handles thumbnail image conversions (e.g., WebP to PNG).

5. Uses mutagen to seamlessly embed album art and metadata directly into the audio file container.

6. Real-time Active Logs: An integrated, scrollable terminal console directly on the web page so you can track download progress and yt-dlp output in real time.

7. Duplicate Detection: Smart parsing to check if the target file already exists in your destination directory before re-downloading.

## Implementation Preview

When a download is processed, the system handles the extraction, converts the artwork, and packages everything cleanly into a single file:

## 🎭 Requirements & Dependencies

Before running the application, make sure you have the necessary system binaries and Python packages installed:

1. FFmpeg Binaries: Must be installed and configured on your system's environmental PATH. (Required by yt-dlp for audio extraction and thumbnail processing).

Python Packages: Install the required libraries via pip:

2. pip install nicegui yt-dlp mutagen

## 👣 Getting Started

1. **Clone the Repository:**
   
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME
   ```
   
## Run the Application:
   
   Once executed, NiceGUI will automatically spin up a local server.

## 👌ow To Use

1. Paste Link: Input your target YouTube video or playlist URL into the Paste YouTube Video URL text area.

2. Set Destination: Update the Destination Folder path to point to your desired local directory (e.g., C:\Users\yourname\Downloads).

3. Configure Quality: Select your preferred audio format (such as opus) and choose your target bitrate (e.g., 320 kbps).

4. Extract: Click the large CONVERT & DOWNLOAD AUDIO button.

5. Monitor: Watch the Active Logs / yt-dlp Console Output section at the bottom for real-time status updates until the progress bar signals completion.

## 🧬Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to submit a pull request or suggest modifications (like dynamic path picking or real-time progress bar parsing).

## 🪪 icense

This project is open-source and available under the MIT License.

Please consider starring their repositories if you find this tool useful!

![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![PowerShell Automation](https://img.shields.io/badge/PowerShell-Automated-lightblue)
![PowerShell Automation](https://img.shields.io/badge/python)