from flask import Flask, request
import pandas as pd
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        file = request.files['inputFile']
        print(file)
    else:
        return "Server is running"

if __name__ == "__main__":
    app.run(debug=True)