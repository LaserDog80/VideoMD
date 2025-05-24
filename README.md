# VideoMD

A collection of small video processing tools built around `ffmpeg` with a minimalist web interface.

## Features

- **Extract first and last frames**: Upload a video and download its first frame.

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
