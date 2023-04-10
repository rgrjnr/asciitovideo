import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import uuid
from frame_extractor import video_to_frames
from image_to_ascii import convert_video

UPLOAD_FOLDER = '/videos'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)

gscale1 = "   .:-=+*#%@"
gscale1 = " .'`^,:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0O#MW&8%B@$"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        unique = str(uuid.uuid4())
        filename = unique + '.mp4'

        if 'file' not in request.files:
            return jsonify({"error": 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": 'No selected file'})

        if file and allowed_file(file.filename):
            file.save(os.path.join('videos', filename))

            video_to_frames(unique)
            convert_video(unique, cols=200, level=gscale1)

            return redirect(url_for('index', video=unique))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route("/video")
def index():
    return render_template('index.html')


@app.route('/json/<path:path>')
def send_js(path):
    return send_from_directory('converted', path)
