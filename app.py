import cv2
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    pass

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/edit", methods=["GET","POST"])
def edit():
    if(request.method == "POST"):
        #upload the file to the server
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error no file received!"
        file = request.files['file']
        operation = request.form['operation']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "No file received!"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(filename, operation)

            return f"Your file is available <a href='/static/{filename}'> here </a>"
    return render_template("index.html")


app.run(debug=True)