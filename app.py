# -*- coding: utf-8 -*-
import os
import openai
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import UnstructuredURLLoader
import unstructured
import pytesseract
from flask import Flask, request

os.environ['OPENAI_API_KEY'] = 'sk-AddYourOWN'

urls = [
    "https://www.urdujini.com/",
    "https://www.ajsoftpk.com/naseem_amjad/",
    "https://www.ajsoftpk.com/naseem_amjad/urdu/",
    "https://www.urdujini.com/demo/"
]

loader = UnstructuredURLLoader(urls=urls)

index = VectorstoreIndexCreator().from_loaders([loader])

query = "Who is Naseem Amjad?"
index.query_with_sources(query)

test1 = index.query_with_sources(query)

print(test1)

#from google.colab import files
#files.upload()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query_text = request.form.get('query_text')
        query_answer = index.query_with_sources(query_text)
        return '''<h1>{}</h1>'''.format(query_answer)


    return '''<form method="POST">
                  <h1>Ask a question about DFW</h1>
                  <h2>The following Web pages are included: </h2>
                    https://www.urdujini.com/<br>
                    https://www.ajsoftpk.com/naseem_amjad/<br>
                    https://www.ajsoftpk.com/naseem_amjad/urdu/<br>
                    https://www.urdujini.com/demo/<br>
                  Query_text: <input type="text" name="query_text"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == "__main__":
    app.run()
