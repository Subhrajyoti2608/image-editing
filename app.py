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
    image = cv2.imread(f"uploads/{filename}")
    match operation:
        case "gray":
            gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            newFileName = f"static/{filename}"
            cv2.imwrite(newFileName, gray)
            return newFileName
        case "cjpg":
            newFileName = f"static/{filename.split('.')[0] + '.jpg'}"
            cv2.imwrite(newFileName, image)
            return newFileName
        case "cpng":
            newFileName = f"static/{filename.split('.')[0] + '.png'}"
            cv2.imwrite(newFileName, image)
            return newFileName
        case "cwebp":
            newFileName = f"static/{filename.split('.')[0] + '.webp'}"
            cv2.imwrite(newFileName, image)
            return newFileName
        



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
        print(request.form)
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
            newFileName=processImage(filename, operation)

            return f"Your file is available <a href='{newFileName}'> here </a>"
    return render_template("index.html")


app.run(debug=True, port=5001)