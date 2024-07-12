# -*- coding: utf-8 -*-
import os
import openai
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import UnstructuredURLLoader
from langchain.document_loaders import UnstructuredPDFLoader
import unstructured
import pytesseract
from flask import Flask, request

os.environ['OPENAI_API_KEY'] = 'sk-AddYourOwnKey'

pdfs = [
    "books-agiliq-com-django-multi-tenant-en-latest.pdf",
    "books-agiliq-com-django-orm-cookbook-en-latest.pdf",
    "books-agiliq-com-djangoprojectscookbook-en-latest.pdf",
    "django-admin-cookbook.pdf",
    "djangoapibook.pdf",
    "The.Python.Journeyman.pdf",
]

pdf_paths =  ["pdfs/" + pdf for pdf in pdfs]
print(pdf_paths)

loader = UnstructuredPDFLoader(pdf_paths[0])
index = VectorstoreIndexCreator().from_loaders([loader])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query_text = request.form.get('query_text')
        query_answer = index.query_with_sources(query_text)
        return '''<h1>{}</h1>'''.format(query_answer)
    return '''<form method="POST">
                  <h1>Ask a question</h1>                  
                  Query_text: <input type="text" name="query_text" style="width: 300px;"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == "__main__":
    app.run()
