from flask import Flask, render_template, request
import os
import uuid
import numpy as np
import cv2
from tensorflow.keras.models import load_model

app = Flask(__name__)

# 📁 Upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🧠 Load trained model
model = load_model("model.h5")   # ⚠️ ensure file exists

# 🏠 Home page
@app.route("/")
def index():
    return render_template("index.html")

# 🔍 Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files.get("file")

        if file is None or file.filename == "":
            return "No file uploaded"

        # 🔥 Unique filename
        filename = str(uuid.uuid4()) + ".jpg"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # 🧠 Image preprocessing (IMPORTANT)
        img = cv2.imread(filepath)
        img = cv2.resize(img, (224, 224))   # ⚠️ same size as training
        img = img / 255.0
        img = np.reshape(img, (1, 224, 224, 3))

        # 🔥 Prediction
        prediction = model.predict(img)

        if prediction[0][0] > 0.5:
            result = "PNEUMONIA"
            confidence = round(float(prediction[0][0]) * 100, 2)
        else:
            result = "NORMAL"
            confidence = round((1 - float(prediction[0][0])) * 100, 2)

        return render_template(
            "result.html",
            result=result,
            confidence=confidence,
            image_path="uploads/" + filename
        )

    except Exception as e:
        return f"ERROR: {str(e)}"

# 🚀 Run
if __name__ == "__main__":
    app.run(debug=True)
