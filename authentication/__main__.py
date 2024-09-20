from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/api/validate/<voter>", methods=["POST"])
def validate(voter):
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = os.path.join(UPLOAD_FOLDER, "webcam_capture.jpg")
        with open(filename, "wb") as f:
            f.write(file.read())
            return jsonify({"message": f"Image received for voter {voter}"}), 200


@app.route("/")
def login():
    return render_template("login.html.jinja")


if __name__ == "__main__":
    app.run(debug=True)
