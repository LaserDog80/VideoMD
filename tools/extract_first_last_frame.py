import os
import subprocess
import uuid


def extract_first_last_frames(input_path, output_dir):
    """Extract the first and last frame of a video using ffmpeg."""
    os.makedirs(output_dir, exist_ok=True)
    video_id = str(uuid.uuid4())
    first_frame = os.path.join(output_dir, f"{video_id}_first.jpg")
    last_frame = os.path.join(output_dir, f"{video_id}_last.jpg")

    # Get video duration
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_path,
        ],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    duration = float(result.stdout.strip())

    # Extract first frame
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-ss",
            "0",
            "-vframes",
            "1",
            first_frame,
        ],
        check=True,
    )

    # Extract last frame slightly before end of video
    last_time = max(duration - 0.04, 0)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-ss",
            str(last_time),
            "-vframes",
            "1",
            last_frame,
        ],
        check=True,
    )

    return first_frame, last_frame


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract first and last frame from a video")
    parser.add_argument("input", help="Path to input video")
    parser.add_argument("output_dir", help="Directory to save frames")
    args = parser.parse_args()

    first, last = extract_first_last_frames(args.input, args.output_dir)
    print("First frame saved to", first)
    print("Last frame saved to", last)
