from flask import Flask, render_template, request
import random
from PIL import Image
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files.get('file')

        if not file:
            return "No file uploaded"

        # Save image
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Open safely
        img = Image.open(file_path)

        # Fake AI result
        result = random.choice(["PNEUMONIA", "NORMAL"])
        confidence = random.randint(85, 98)

        return render_template(
            'result.html',
            result=result,
            confidence=confidence,
            image_path="uploads/" + file.filename
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
