from flask import Flask, request, send_file, send_from_directory
import os
from tools.extract_first_last_frame import extract_first_last_frames

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


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True)
