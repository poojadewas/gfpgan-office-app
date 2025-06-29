import os
from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Load Hugging Face API Token
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/TencentARC/GFPGAN"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    output_image = None

    if request.method == 'POST':
        image = request.files['image']
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        input_path = os.path.join(upload_folder, image.filename)
        output_path = os.path.join(upload_folder, f"restored_{image.filename}")
        image.save(input_path)

        with open(input_path, 'rb') as f:
            response = requests.post(API_URL, headers=HEADERS, data=f)

        if response.status_code == 200:
            with open(output_path, 'wb') as out:
                out.write(response.content)
            output_image = output_path
        else:
            return f"Error from Hugging Face API: {response.status_code} - {response.text}"

    return render_template("index.html", output_image=output_image)

# Needed for gunicorn deployment
if __name__ == '__main__':
    app.run(debug=True)
