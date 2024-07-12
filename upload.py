from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/myuploads' # replace with your desired upload folder path

@app.route('/upload', methods=['POST'])
def upload():
    import os

    print(request.files) # this will print out the received name, temp name, type, size, etc.

    size = request.files['audio_data'].content_length # the size in bytes
    input_file = request.files['audio_data'].filename # temporary name that Flask gave to the uploaded file
    output_file = secure_filename(request.files['audio_data'].filename) + ".wav" # letting the client control the filename is a rather bad idea, hence using a secure filename.

    # move the file from temp name to local folder using output name
    request.files['audio_data'].save(os.path.join(app.config['UPLOAD_FOLDER'], output_file))

    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
