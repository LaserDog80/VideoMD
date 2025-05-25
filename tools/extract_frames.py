import os
import subprocess
import uuid


def get_video_metadata(input_path):
    """Return basic metadata for the first video stream using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate,pix_fmt,sample_aspect_ratio",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_path,
        ],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().splitlines()
    width = int(lines[0]) if len(lines) > 0 else 0
    height = int(lines[1]) if len(lines) > 1 else 0
    fps = lines[2] if len(lines) > 2 else "0/1"
    if "/" in fps:
        num, denom = fps.split("/")
        fps = float(num) / float(denom)
    else:
        fps = float(fps)
    fmt = lines[3] if len(lines) > 3 else ""
    par = lines[4] if len(lines) > 4 else ""
    return {
        "width": width,
        "height": height,
        "fps": fps,
        "format": fmt,
        "pixel_aspect_ratio": par,
    }


def extract_frames(input_path, output_dir, interval=1, mode="seconds"):
    """Extract frames from a video at a given interval.

    Args:
        input_path (str): Path to the input video.
        output_dir (str): Directory where frames will be saved.
        interval (float): Interval value depending on ``mode``.
        mode (str): ``"seconds"`` to grab one frame every ``interval`` seconds or
            ``"frames"`` to grab every ``interval``-th frame.
    Returns:
        str: Directory containing the extracted frames.
    """
    os.makedirs(output_dir, exist_ok=True)
    video_id = str(uuid.uuid4())
    frame_dir = os.path.join(output_dir, video_id)
    os.makedirs(frame_dir, exist_ok=True)
    output_pattern = os.path.join(frame_dir, "%04d.jpg")

    if mode == "seconds":
        vf = f"fps=1/{interval}"
        cmd = ["ffmpeg", "-y", "-i", input_path, "-vf", vf, output_pattern]
    else:
        vf = f"select=not(mod(n\\,{int(interval)}))"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            vf,
            "-vsync",
            "vfr",
            output_pattern,
        ]

    subprocess.run(cmd, check=True)
    return frame_dir


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract frames from a video")
    parser.add_argument("input", help="Path to input video")
    parser.add_argument("output_dir", help="Directory to save frames")
    parser.add_argument(
        "--interval",
        type=float,
        default=1,
        help="Interval in seconds or frames depending on mode",
    )
    parser.add_argument(
        "--mode",
        choices=["seconds", "frames"],
        default="seconds",
        help="Extraction mode",
    )
    args = parser.parse_args()

    dir_path = extract_frames(args.input, args.output_dir, args.interval, args.mode)
    print("Frames saved to", dir_path)
