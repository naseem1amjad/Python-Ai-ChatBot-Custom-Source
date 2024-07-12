import os
import openai
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import PyPDFDirectoryLoader
import unstructured
import pytesseract
from flask import Flask, request

os.environ['OPENAI_API_KEY'] = 'sk-AddYourOwnKey'

pdf_paths =  "pdfs/"
print(pdf_paths)

loader = PyPDFDirectoryLoader(pdf_paths)

index = VectorstoreIndexCreator().from_loaders([loader])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit():
    my_form='''<form method="POST">
                  <h1>Ask a question</h1>                  
                  Query_text: <input type="text" name="query_text" style="width: 300px;"><br>
                  <input type="reset" value="Reset"><input type="submit" value="Submit"><br>
              </form>'''
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query_text = request.form.get('query_text')
        query_answer = index.query_with_sources(query_text)
        return my_form+'''<h1>{}</h1>'''.format(query_answer)
    return my_form

@app.route('/upload', methods=['POST'])
def uploadAudio():
    import os

    print(request.files) # this will print out the received name, temp name, type, size, etc.

    size = request.files['audio_data'].content_length # the size in bytes
    input_file = request.files['audio_data'].filename # temporary name that Flask gave to the uploaded file
    output_file = secure_filename(request.files['audio_data'].filename) + ".wav" # letting the client control the filename is a rather bad idea, hence using a secure filename.

    # move the file from temp name to local folder using output name
    request.files['audio_data'].save(os.path.join(app.config['UPLOAD_FOLDER'], output_file))

    return 'File uploaded successfully!'
    
if __name__ == "__main__":
    app.run()
