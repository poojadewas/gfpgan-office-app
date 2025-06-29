import os
import replicate
from flask import Flask, render_template, request

# Safely access API token from environment variable
if not os.environ.get("REPLICATE_API_TOKEN"):
    raise Exception("Missing REPLICATE_API_TOKEN environment variable.")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_url = None
    if request.method == "POST":
        image = request.files["image"]
        image.save("input.jpg")

        with open("input.jpg", "rb") as img_file:
            output_url = replicate.run(
                "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
                input={"img": img_file}
            )

    return render_template("index.html", output_url=output_url)

if __name__ == "__main__":
    app.run(debug=True)
