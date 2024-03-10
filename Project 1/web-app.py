from flask import Flask, request, redirect
import pandas as pd
import warnings
import requests


warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)

classResDict = {}

classRes = pd.read_csv('Classification Results.csv')

for ele in classRes.iterrows():
    classResDict[ele[1][0]] = ele[1][1]


@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method == "POST":
        form = request.files['inputFile']
        # filename = form.filename.split('.')[0]
        resp = requests.post('http://54.242.102.215:80', files=form)
        # ans_dict = requests.get('http://54.242.102.215:80')
        # return "{}:{}".format(filename, ans_dict[filename])
        return resp
    else:
        return "Server is running!"
    
if __name__ == "__main__":
    app.run(debug=False)