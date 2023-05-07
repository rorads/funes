"""
Demo pipeline to tie together the desired APIs
"""

import traceback
import logging
from langchain.embeddings import HuggingFaceEmbeddings
import os
import argparse
# import pandas as pd
from langchain.vectorstores import FAISS
from langchain.chains import AnalyzeDocumentChain
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader

# set the logging level to INFO to see the similarity search results
logging.basicConfig(level=logging.DEBUG)

# use argparse to pass in the path to the PDF file. Assume that the
# path is passed with the --pdf_path flag
parser = argparse.ArgumentParser()
parser.add_argument("--pdf_path", type=str, required=True)
parser.add_argument("--output_dir", type=str,
                    default="data/intermediate/test_pdf")
parser.add_argument('--write_pages', action=argparse.BooleanOptionalAction)

args = parser.parse_args()
PDF_PATH = args.pdf_path
OUTPUT_DIR = args.output_dir

loader = PyMuPDFLoader(PDF_PATH)
data = loader.load()

print(len(data))

if args.write_pages:
    # Save pages to individual files
    if not os.path.exists("data/intermediate/test_pdf"):
        os.makedirs("data/intermediate/test_pdf")

    # use os to wipe the contents of the directory above, if it exists
    for file in os.listdir("data/intermediate/test_pdf"):
        os.remove(os.path.join("data/intermediate/test_pdf", file))

    for page in data:
        path = f"data/intermediate/test_pdf/p_{page.metadata['page_number']}.txt"  # noqa: E501
        with open(path, "w") as f:
            f.write(page.page_content)

# Optional: Embedding and similarity search: If you need to perform similarity
# searches among the chunks, you can use LangChain's FAISS vector store along
# with OpenAIEmbeddings python.langchain.com:


model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)


try:
    # Replace the OpenAIEmbeddings() call with the `get_embeddings` function
    faiss_index = FAISS.from_documents(data, hf)
    docs = faiss_index.similarity_search(
        "digital and data infrastructure", k=2)
except Exception as e:
    # Capture the stack trace
    print(e)
    stack_trace = traceback.format_exc()
    print(stack_trace)


# Unused currently
# faiss_index = FAISS.from_documents(data, OpenAIEmbeddings())  # hot
# docs = faiss_index.similarity_search("Your search query", k=2)

for doc in docs:
    print(doc.page_content)

# Optional: Summarize using GPT and LangChain: If you want to generate a
# summary of the long PDF, you can use the AnalyzeDocumentChain class with
# chain_type='map_reduce' and process the extracted text.


chain = AnalyzeDocumentChain(chain_type="map_reduce")
summary = chain.run(data)
print(summary)

# This pipeline allows you to parse a long PDF, split it into chunks, save the
# chunks to individual files, and optionally perform similarity searches or
# generate a summary using GPT and LangChain. Note that the quality of the
# summary may not be as exciting as that generated by ChatGPT with an
# appropriate prompt, but it can still provide a useful starting point for
# understanding the document's content
