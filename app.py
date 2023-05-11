import os
from flask import Flask, render_template, request
from flask_cors import CORS

# import our OCR function
from ocr_core import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
CORS(app)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return {'hello': 'world'}

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return  {'msg':'No file selected'}
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return {'msg': 'no file selected'}

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return  {'msg': 'Successfully processed',  "extracted_text":extracted_text}
    elif request.method == 'GET':
        return {'msg':'method not alowid'}

if __name__ == '__main__':
    app.run()