from flask import Flask, render_template, request
from werkzeug import secure_filename
from cluster import get_dominant
from imageio import imread
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get('file')
        if f is None:
        	return "No Image Uploaded!!!"
        f.save(secure_filename(f.filename))
        img = imread(secure_filename(f.filename))
        os.remove(secure_filename(f.filename))
        tot, name, centroids_conc = get_dominant(img)
        return render_template("main.html", after=True, colors=centroids_conc, tot=tot, name=name)
    return render_template("main.html", after=False)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1,firefox=1'
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


