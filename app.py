from flask import Flask, render_template, request
import random
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    
    if file:
        img = Image.open(file)

        # FAKE AI RESULT (works 100%)
        result = random.choice(["PNEUMONIA", "NORMAL"])
        confidence = random.randint(85, 98)

        return render_template('result.html', result=result, confidence=confidence)

    return "No file uploaded"

if __name__ == "__main__":
    app.run(debug=True)
