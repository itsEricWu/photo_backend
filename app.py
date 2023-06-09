import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory, render_template
import json
import flask_cors as cors
import cv2

UPLOAD_FOLDER = 'uploads'
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors.CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")
        if len(files) == 0:
            return json.dumps({"error": "No file selected"})
        for file in files:
            if file.filename == '':
                return json.dumps({"error": "No file selected"})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('upload.html')
    return render_template('upload.html')

@app.route('/get_name_list', methods=['GET'])
def get_name_list():
    response = []
    for file in os.listdir(app.config["UPLOAD_FOLDER"]):
        try:
            h, w, c = cv2.imread(os.path.join(app.config["UPLOAD_FOLDER"], file)).shape
            response.append({"name": file, "width": w, "height": h})    
        except:
            continue
    return json.dumps(response)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

if __name__ == "__main__":
    app.run(debug=True)