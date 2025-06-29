import replicate
import os
from flask import Flask, render_template, request

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_Af1yG4vRtHf7BVS47ZalRdSVZYttdQX0qdmdR"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_url = None

    if request.method == "POST":
        # Save uploaded image
        image = request.files["image"]
        image.save("input.jpg")

        # Run Replicate model
        output_url = replicate.run(
            "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
            input={"img": open("input.jpg", "rb")}
        )

    return render_template("index.html", output_url=output_url)

if __name__ == "__main__":
    app.run(debug=True)
