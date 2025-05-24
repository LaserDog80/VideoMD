import os
import subprocess
import uuid


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
