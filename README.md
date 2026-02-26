# 🎬 EZ Youtube Downloader  

An extremely easy-to-use **YouTube video/audio downloader** for everyone. 

Are you intimidated by the thought of using a terminal but find it cool? Are you tired of searching for a good online YouTube downloader that is not bogged down by malicious ads? Well, this program is for you!

Just download the executable, start saving your favorite videos or audio tracks right away, and look cool doing it!

---

## Quick Start (Beginner Friendly)

1. **Download the latest `.exe` file** from the [Releases](https://github.com/kncabatuan/EZ-Youtube-Downloader/releases) page.  

2. Extract it anywhere and double-click the `.exe` to run the program.

   ⚡ Tip: If FFmpeg is missing, the program will want to set it up for you. Don't be scared, just enter "y", let it download, and you're golden.

3. Follow the on-screen prompts to:  
   - Choose between **single** or **batch** download
   - Choose between **video** or **audio only**
   - Paste a **YouTube URL** (or follow the instructions if batch download)
   - Watch it download automatically into your **Downloads folder**  
   
4. Done! Your video/audio is ready to enjoy. 🍿

Note: If a video is downloaded in 360p resolution, it may be due to restrictions such as:
   - Geo-restrictions
   - Age restrictions 
   - Members-only content
   - Platform-imposed quality limitations

---

## Features

- High-quality video downloads (up to 1080p).
- High-bitrate audio extraction.
- Automatic FFmpeg installation and configuration.
- Automatic merging of video and audio streams.
- Smart format detection using yt-dlp.
- Standalone Windows executable.
- Minimal setup required.

---

## Running From Source

If you want to work with the **source code**:  

```bash
git clone https://github.com/kncabatuan/EZ-Youtube-Downloader.git
cd EZ-Youtube-Downloader
pip install -r requirements.txt
python ez_youtube.py 
```   

## Tips

Make sure Python 3.10+ is installed if running from source.

## Contributing

If you want to improve my work, you are very welcome to do so! I'll be waiting for those pull requests 😃

## ⚠ Disclaimer

This tool is for educational and personal use only.  
Please respect YouTube’s Terms of Service and copyright laws in your country.  
The developer is not responsible for misuse of this software.

## 📜 License

This project is licensed under the MIT License.