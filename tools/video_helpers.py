import os
import subprocess
import json
import uuid
import glob


def get_video_metadata(input_path):
    """Return metadata for a video using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            input_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return json.loads(result.stdout)


def extract_frames(input_path, output_root, interval, mode="frames"):
    """Extract frames from a video at a given interval.

    Parameters
    ----------
    input_path : str
        Path to the input video file.
    output_root : str
        Directory where extracted frames should be saved.
    interval : int or float
        Interval between frames. Interpretation depends on ``mode``.
    mode : str
        Either ``"frames"`` to grab every Nth frame or ``"seconds"`` to grab
        one frame every N seconds.
    Returns
    -------
    str
        Directory containing the extracted frames.
    list[str]
        List of frame file paths.
    """

    output_dir = os.path.join(output_root, str(uuid.uuid4()))
    os.makedirs(output_dir, exist_ok=True)

    if mode == "frames":
        filter_str = f"select=not(mod(n\,{int(interval)}))"
    else:  # seconds
        filter_str = f"fps=1/{float(interval)}"

    frame_pattern = os.path.join(output_dir, "frame_%05d.jpg")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            filter_str,
            "-vsync",
            "vfr",
            frame_pattern,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    frames = sorted(glob.glob(os.path.join(output_dir, "frame_*.jpg")))
    return output_dir, frames
