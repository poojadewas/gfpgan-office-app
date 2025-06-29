import replicate
import os
from flask import Flask, render_template, request

# Ensure the token is used from environment
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_url = None
    if request.method == "POST":
        image = request.files["image"]
        image_path = "input.jpg"
        image.save(image_path)

        # Use file as input
        with open(image_path, "rb") as img_file:
            output = replicate.run(
                "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
                input={"img": img_file}
            )
            output_url = output  # Usually a list of URLs

    return render_template("index.html", output_url=output_url)
