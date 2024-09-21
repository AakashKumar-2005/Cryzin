from flask import Flask, render_template, jsonify, request
import face
import os
import tempfile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/api/validate/<voter>", methods=["POST"])
def validate(voter):
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        res = face.verify(voter, temp.name)
    os.remove(temp.name)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
