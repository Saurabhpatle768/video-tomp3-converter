from flask import Flask, render_template, request, send_file, jsonify
import os
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Route for homepage
@app.route("/")
def index():
    return render_template("index.html")

# Handle upload + conversion
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # simulate upload progress (for demo purpose)
    for i in range(1, 101, 25):
        time.sleep(0.2)

    # Convert video → mp3
    clip = VideoFileClip(filepath)
    mp3_filename = os.path.splitext(filename)[0] + ".mp3"
    output_path = os.path.join(app.config["OUTPUT_FOLDER"], mp3_filename)

    # simulate conversion progress
    for i in range(1, 101, 25):
        time.sleep(0.3)

    clip.audio.write_audiofile(output_path)
    clip.close()

    return jsonify({"download_url": f"/download/{mp3_filename}"})


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(app.config["OUTPUT_FOLDER"], filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
