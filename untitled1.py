# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QPeD72D2pUCYa_v4Vjbw3Qa41-3eWuWq

# Lang-Chain
"""

!pip install pymupdf

import fitz

!pip uninstall -y faiss faiss-gpu

doc = fitz.open("/content/Acko-Group-Health-Insurance.pdf")
s = []
for i in doc.pages():
  for j in i.get_text().split('\n'):
    s.append(j)

!pip install faiss-gpu-cu11

!pip install langchain
!pip install transformers
!pip install sentence_transformers

!pip install langchain-community

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
import os

pip install --upgrade transformers

# db = FAISS.from_documents(s, embeddings)
vector_store = FAISS.from_texts(s, embedding=HuggingFaceEmbeddings())



retriver = vector_store.as_retriever()

# print(retriver.get_relevant_documents('what is akaike'))

from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.chains import RetrievalQA

tokenizer  = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=1000,
    top_k = 50,
    temperature=0.5,
    truncation = True
)

gpt2_model = HuggingFacePipeline(pipeline=pipe)
qa_chain = RetrievalQA.from_chain_type(llm=gpt2_model, chain_type="stuff", retriever=retriver, return_source_documents=True)

while 1:
  query = input()
  if query == 'exit':
    break
  response = qa_chain(query)
  print(response['result'], response['source_documents'])

