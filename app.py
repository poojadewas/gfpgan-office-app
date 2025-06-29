from flask import Flask, render_template, request, redirect
import replicate
import os

app = Flask(__name__)

REPLICATE_API_TOKEN = os.environ.get("r8_8JNN22uZfVh9DqKbtOMnXlYInx1hs7l3WDsNU")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"]
        image.save("input.jpg")

        output_url = replicate.run(
            "tencentarc/gfpgan",
            input={"img": open("input.jpg", "rb")}
        )

        return render_template("index.html", output_url=output_url)
    return render_template("index.html", output_url=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
