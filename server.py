from flask import Flask, request, send_file, send_from_directory, jsonify
import os
import uuid
import shutil
from tools.extract_first_last_frame import extract_first_last_frames
from tools.video_helpers import get_video_metadata, extract_frames

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
OUTPUT_FOLDER = os.path.join(os.getcwd(), "outputs")


@app.route("/upload", methods=["POST"])
def upload_video():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)
    first_frame, _ = extract_first_last_frames(input_path, OUTPUT_FOLDER)
    return send_file(first_frame, mimetype="image/jpeg")


@app.route("/metadata", methods=["POST"])
def video_metadata():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)
    data = get_video_metadata(input_path)
    return jsonify(data)


@app.route("/extract_frames", methods=["POST"])
def frames_endpoint():
    file = request.files.get("file")
    interval = request.form.get("interval", type=float)
    mode = request.form.get("mode", "frames")
    if not file or interval is None:
        return "Missing file or interval", 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    frames_dir, _ = extract_frames(input_path, OUTPUT_FOLDER, interval, mode)

    zip_basename = os.path.join(OUTPUT_FOLDER, str(uuid.uuid4()))
    zip_path = shutil.make_archive(zip_basename, "zip", frames_dir)
    return send_file(zip_path, mimetype="application/zip", as_attachment=True, download_name="frames.zip")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True)
