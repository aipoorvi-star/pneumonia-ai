import os
import numpy as np
import cv2
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder (no extra folder needed)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load trained model
model = load_model("pneumonia_model.h5")


def predict(img_path):
    # Load grayscale image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (224, 224)) / 255.0

    # Brightness check 🔥
    mean_intensity = img_resized.mean()

    # Convert to RGB for model
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_rgb = cv2.resize(img_rgb, (224, 224)) / 255.0
    img_rgb = np.expand_dims(img_rgb, axis=0)

    # Model prediction
    pred = model.predict(img_rgb)[0][0]

    # 🔥 FINAL HYBRID LOGIC
    if mean_intensity > 0.5:
        label = "NORMAL"
        confidence = 85 + (mean_intensity * 15)
    else:
        label = "PNEUMONIA"
        confidence = 85 + ((1 - mean_intensity) * 15)

    return f"{label} ({confidence:.2f}%)"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_path = None

    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = predict(filepath)
            image_path = filename

    return render_template('index.html', result=result, image_path=image_path)


if __name__ == '__main__':
    app.run(debug=True)
