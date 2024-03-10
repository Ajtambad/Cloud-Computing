from flask import Flask, request
import pandas as pd
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)

classResDict = {}
ans_dict = {}

classRes = pd.read_csv('Classification Results.csv')

for ele in classRes.iterrows():
    classResDict[ele[1][0]] = ele[1][1]


@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        form = request.files['inputFile']
        filename = form.filename.split('.')[0]
        ans_dict[filename] = classResDict[filename]
        # return "{}:{}".format(filename, classResDict[filename])
        requests.post('http://44.197.210.121:80', data=ans_dict)
    else:
        return "Server is running"

if __name__ == "__main__":
    app.run(debug=True)