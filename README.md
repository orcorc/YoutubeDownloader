# YouTube Downloader

A lightweight web app for downloading YouTube videos and audio at source quality. Built with Python, Flask, and yt-dlp.

## Features

- **Video download** — Best video + audio merged into MP4 at source quality
- **Audio download** — Best audio extracted as MP3
- **Video preview** — Shows thumbnail, title, uploader, duration, and view count before downloading
- **Dark themed UI** — Clean, responsive interface that works on desktop and mobile
- **Auto-discovers FFmpeg** — Automatically finds FFmpeg even if it's not on your system PATH

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/) (make sure to check "Add Python to PATH" during install)
- [FFmpeg](https://ffmpeg.org/) (required for merging video/audio streams and MP3 conversion)

### Installing FFmpeg on Windows

```
winget install Gyan.FFmpeg
```

## Setup

1. **Clone or download** this project

2. **Install Python dependencies:**

   ```
   cd "Youtube Downloader"
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```
   python app.py
   ```

4. **Open your browser** and go to:

   ```
   http://localhost:5000
   ```

## Usage

1. Paste a YouTube URL into the input field
2. Click **Fetch** (or press Enter) to load video info
3. Click **Video (MP4)** or **Audio (MP3)** to download

Downloaded files are temporarily stored in the `downloads/` folder inside the project directory.

## Project Structure

```
Youtube Downloader/
├── app.py               # Flask backend with yt-dlp integration
├── requirements.txt     # Python dependencies (flask, yt-dlp)
├── templates/
│   └── index.html       # Web UI (single-page, self-contained)
└── downloads/           # Temporary download output (auto-created)
```

## API Endpoints

| Method | Endpoint        | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | `/`             | Serves the web UI                    |
| POST   | `/api/info`     | Fetches video metadata (title, thumbnail, etc.) |
| GET    | `/api/download` | Downloads video or audio file        |

### `POST /api/info`

**Body:** `{ "url": "https://www.youtube.com/watch?v=..." }`

**Response:** `{ "title", "thumbnail", "duration", "uploader", "view_count", "url" }`

### `GET /api/download`

**Params:**
- `url` — YouTube video URL
- `mode` — `video` (default) or `audio`

## Troubleshooting

### "ffmpeg is not installed"

The app auto-discovers FFmpeg from WinGet install locations. If it still can't find it:

- Restart your terminal after installing FFmpeg so the PATH updates
- Or install FFmpeg and ensure `ffmpeg` is accessible from your command line (`ffmpeg -version`)

### "No supported JavaScript runtime"

This is a yt-dlp warning. It still works but you may get better format selection by installing [Deno](https://deno.land/):

```
winget install DenoLand.Deno
```

## License

This project is licensed under the [MIT License](LICENSE).
