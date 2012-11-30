import os
import random
from SimpleCV import *
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import render_template

UPLOAD_FOLDER = "static/"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "PNG", "JPG", "JPEG"])
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
haarcascade = HaarCascade("face")

def allowed_file(filename):
     return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

@app.route("/sandeep/upload/", methods=["GET", "POST"])
def upload_file():
    radnum = random.randrange(100000,200000);
    if request.method == "POST": 
    	file = request.files["file"]
    	if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename.split(".")[0]+str(radnum)+"."+filename.split(".")[1]))
            image = Image(os.path.join(app.config["UPLOAD_FOLDER"], filename.split(".")[0]+str(radnum)+"."+filename.split(".")[1]))
            faces = image.findHaarFeatures(haarcascade)
            if faces:
                for i in faces:
                    i.draw()
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename.split(".")[0]+str(radnum)+"output"+"."+filename.split(".")[1]))
                return render_template("result.html", name=filename.split(".")[0]+str(radnum)+"output"+"."+filename.split(".")[1])
            else :
                return render_template("result.html", name="noface.png")

@app.route("/sandeep/")
def hello_world():
    return render_template("index.html")

if __name__ == "__main__":
    app.run("ec2-23-20-93-69.compute-1.amazonaws.com",443)
