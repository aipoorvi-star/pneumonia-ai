from flask import Flask, render_template, request
import os
import uuid
import random
from PIL import Image

app = Flask(__name__)

# folder setup
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# home
@app.route("/")
def index():
    return render_template("index.html")

# predict
@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("file")

    if file is None or file.filename == "":
        return "No file uploaded"

    # unique filename
    filename = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # save file
    file.save(filepath)

    # verify image (prevents crash)
    try:
        img = Image.open(filepath)
        img.verify()
    except:
        return "Invalid image file"

    # fake result
    result = random.choice(["PNEUMONIA", "NORMAL"])
    confidence = random.randint(85, 98)

    return render_template(
        "result.html",
        result=result,
        confidence=confidence,
        image_path="uploads/" + filename
    )

# run
if __name__ == "__main__":
    app.run(debug=True)
