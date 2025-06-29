import os
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Read Hugging Face token from environment (Render dashboard)
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/TencentARC/GFPGAN"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        image_path = os.path.join('static/uploads', image.filename)
        image.save(image_path)

        with open(image_path, 'rb') as f:
            response = requests.post(API_URL, headers=HEADERS, data=f)

        if response.status_code == 200:
            output_path = os.path.join('static/uploads', 'restored_' + image.filename)
            with open(output_path, 'wb') as out:
                out.write(response.content)
            return render_template("index.html", output_image=output_path)
        else:
            return f"Error: {response.status_code} - {response.text}"

    return render_template("index.html", output_image=None)

if __name__ == '__main__':
    app.run(debug=True)
