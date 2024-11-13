import random
import string
import json

from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)
shorterned_urls = {}

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url


@app.route("/", methods =["GET", "POST"])
def index():
    if request.methods == "POST":
        long_url = request.form["long_url"]
        short_url = generate_short_url()
        while short_url in shorterned_urls:
            short_url = generate_short_url()

    shorterned_urls[short_url] = long_url
    with open("urls.json", "w")as f:
        json.dump(shorterned_urls, f)
    return "Shortened URL: {request.url_root}{short_url}"
    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shorterned_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    

    if __name__ == "__main__":
        with open ("urls.json", "r") as f:
            shorterned_urls = json.load(f) 
        app.run(debug=True)