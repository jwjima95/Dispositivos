import os
from flask import Flask, request, jsonify
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ['OPENAI_API_KEY'] = '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'
default_doc_name = 'doc.pdf'

@app.route('/process', methods=['POST'])
def process_doc():
    pdf_file = request.files.get('pdf')
    question = request.form.get('question')

    pdf_path = f'./{default_doc_name}'
    pdf_file.save(pdf_path)

    loader = PyPDFLoader(pdf_path)
    doc = loader.load_and_split()

    db = Chroma.from_documents(doc, embedding=OpenAIEmbeddings())

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=db.as_retriever())
    answer = qa.run(question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
