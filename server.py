from flask import Flask, request, send_file, send_from_directory, jsonify, after_this_request
import os
import subprocess
import uuid
import shutil
import json
from tools.extract_first_last_frame import extract_first_last_frames
from tools.extract_frames import extract_frames, get_video_metadata

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
def metadata():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    temp_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{file.filename}")
    file.save(temp_path)
    try:
        meta = get_video_metadata(temp_path)
    finally:
        os.remove(temp_path)
    return jsonify(meta)


@app.route("/extract_frames", methods=["POST"])
def extract_frames_route():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400
    interval = request.form.get("interval", type=float, default=1)
    mode = request.form.get("mode", "seconds")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{file.filename}")
    file.save(input_path)

    frame_dir = extract_frames(input_path, OUTPUT_FOLDER, interval, mode)
    zip_base = os.path.join(OUTPUT_FOLDER, str(uuid.uuid4()))
    zip_path = shutil.make_archive(zip_base, "zip", frame_dir)

    @after_this_request
    def cleanup(response):
        try:
            os.remove(input_path)
        except OSError:
            pass
        shutil.rmtree(frame_dir, ignore_errors=True)
        try:
            os.remove(zip_path)
        except OSError:
            pass
        return response

    return send_file(zip_path, as_attachment=True, download_name="frames.zip")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True)
