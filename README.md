# VideoMD

A collection of small video processing tools built around `ffmpeg` with a minimalist web interface.

## Features

- **Extract first and last frames**: `/upload` returns the first frame of the uploaded video.
- **Video metadata**: `/metadata` returns JSON metadata extracted with `ffprobe`.
- **Frame extraction**: `/extract_frames` extracts frames at a given interval and returns them as a ZIP file.

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
4. Open [http://localhost:5000](http://localhost:5000) in a browser to use the simple uploader.

Uploaded files and extracted frames are saved in the `uploads` and `outputs` folders respectively.
