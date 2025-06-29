from flask import Flask, render_template, request
import os
import replicate

app = Flask(__name__, static_url_path='', static_folder='static')

# Ensure upload folder exists on server (Render or local)
os.makedirs("static/uploads", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    output_url = None

    if request.method == "POST":
        image = request.files["image"]
        upload_path = os.path.join("static", "uploads", image.filename)
        image.save(upload_path)

        # Create the full URL for the hosted image
        image_url = f"https://gfpgan-office-app.onrender.com/{upload_path}"

        # Call Replicate API with the public image URL
        output = replicate.run(
            "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
            input={"img": image_url}
        )

        output_url = output  # usually a list of image URLs

    return render_template("index.html", output_url=output_url)
