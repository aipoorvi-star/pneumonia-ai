from flask import Flask, render_template, request
import random
from PIL import Image

app = Flask(__name__)

# HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')


# PREDICT ROUTE
@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files.get('file')

        if not file:
            return "No file uploaded"

        # SAFE IMAGE OPEN
        img = Image.open(file.stream)

        # FAKE AI RESULT (WORKING)
        result = random.choice(["PNEUMONIA", "NORMAL"])
        confidence = random.randint(85, 98)

        return render_template('result.html', result=result, confidence=confidence)

    except Exception as e:
        return f"Error: {str(e)}"


# RUN APP
if __name__ == "__main__":
    app.run()
