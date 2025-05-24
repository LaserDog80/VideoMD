# VideoMD

A collection of small video processing tools built around `ffmpeg` with a minimalist web interface.

## Features

- **Extract first and last frames**: Upload a video and download its first frame.
- **Extract arbitrary frames**: Use `tools/extract_frames.py` or the `/extract_frames` endpoint to grab frames at specific timestamps.
- **View video metadata**: Upload a file and use `/metadata` to get duration, resolution and more.

More tools can be added as standalone scripts in the `tools` directory.

## Usage

1. Install dependencies:
   ```bash
   pip install Flask
   ```
2. Ensure `ffmpeg` and `ffprobe` are installed and available in your `PATH`.
3. Run the server:
   ```bash
   python server.py
   ```
4. Open [http://localhost:5000](http://localhost:5000) in a browser and upload a video file.

Extracted frames will be saved in the `outputs` folder.

## Command-line tools

`tools/extract_frames.py` can extract one or more frames from a video. Basic usage:

```bash
python tools/extract_frames.py input.mp4 outputs/ --timestamps 0 3.2 10
```

This will save three JPEGs at the given timestamps in seconds. Alternatively, extract a frame every N seconds:

```bash
python tools/extract_frames.py input.mp4 outputs/ --interval 5
```

## Server API

The Flask server exposes two endpoints:

- `POST /metadata` – upload a video to receive a JSON summary including duration, codec and resolution.
- `POST /extract_frames` – upload a video (optionally providing timestamps or an interval) and download a zip archive containing the requested frames.

Example usage:

```bash
# Get metadata
curl -F file=@video.mp4 http://localhost:5000/metadata

# Extract frames every 5 seconds
curl -F file=@video.mp4 -F interval=5 http://localhost:5000/extract_frames -o frames.zip
```

## Web interface

The index page offers checkboxes to request metadata and to extract frames at a fixed interval. After an upload completes, the page displays the returned metadata so you can verify the video’s properties.
