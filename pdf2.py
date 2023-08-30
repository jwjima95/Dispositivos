import os
from flask import Flask, request, jsonify
from PyPDF2 import PdfMerger
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ['OPENAI_API_KEY'] = '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'
default_merged_doc_name = 'merged_doc.pdf'

@app.route('/process', methods=['POST'])
def process_docs():
    pdf_file1 = request.files.get('pdf1')
    pdf_file2 = request.files.get('pdf2')
    question = request.form.get('question')

    pdf_path1 = f'./pdf1.pdf'
    pdf_path2 = f'./pdf2.pdf'
    pdf_file1.save(pdf_path1)
    pdf_file2.save(pdf_path2)

    merger = PdfMerger()
    merger.append(pdf_path1)
    merger.append(pdf_path2)
    merged_pdf_path = f'./{default_merged_doc_name}'
    merger.write(merged_pdf_path)
    merger.close()

    loader = PyPDFLoader(merged_pdf_path)
    doc = loader.load_and_split()

    db = Chroma.from_documents(doc, embedding=OpenAIEmbeddings())

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=db.as_retriever())
    answer = qa.run(question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
