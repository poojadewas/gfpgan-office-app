import replicate
import os
from flask import Flask, render_template, request

# Use token from environment variable
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_url = None

    if request.method == "POST":
        image = request.files["image"]
        image_path = "input.jpg"
        image.save(image_path)

        with open(image_path, "rb") as img_file:
            output_url = replicate.run(
                "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
                input={"img": img_file}
            )

    return render_template("index.html", output_url=output_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
