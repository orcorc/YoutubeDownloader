import os
import re
import shutil
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Ensure ffmpeg is on PATH (winget installs may not be in current shell's PATH)
FFMPEG_LOCATION = None
if not shutil.which("ffmpeg"):
    _winget_ffmpeg = os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages"
    )
    if os.path.isdir(_winget_ffmpeg):
        for root, dirs, files in os.walk(_winget_ffmpeg):
            if "ffmpeg.exe" in files:
                FFMPEG_LOCATION = root
                os.environ["PATH"] = root + os.pathsep + os.environ.get("PATH", "")
                break


def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()


def format_duration(seconds):
    if not seconds:
        return "Unknown"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info", methods=["POST"])
def video_info():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "duration": format_duration(info.get("duration")),
            "uploader": info.get("uploader", "Unknown"),
            "view_count": info.get("view_count", 0),
            "url": url,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/download")
def download():
    url = request.args.get("url", "").strip()
    mode = request.args.get("mode", "video")  # "video" or "audio"

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Clean up old files in download dir
    for f in os.listdir(DOWNLOAD_DIR):
        try:
            os.remove(os.path.join(DOWNLOAD_DIR, f))
        except OSError:
            pass

    base_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
    }
    if FFMPEG_LOCATION:
        base_opts["ffmpeg_location"] = FFMPEG_LOCATION

    if mode == "audio":
        ydl_opts = {
            **base_opts,
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",  # best quality
            }],
        }
    else:
        ydl_opts = {
            **base_opts,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = sanitize_filename(info.get("title", "download"))

        # Find the downloaded file
        files = os.listdir(DOWNLOAD_DIR)
        if not files:
            return jsonify({"error": "Download failed - no file produced"}), 500

        filepath = os.path.join(DOWNLOAD_DIR, files[0])
        ext = os.path.splitext(files[0])[1]
        download_name = f"{title}{ext}"

        return send_file(
            filepath,
            as_attachment=True,
            download_name=download_name,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("YouTube Downloader running at http://localhost:5000")
    app.run(debug=True, port=5000)
