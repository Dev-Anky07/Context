from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

loader = PyPDFLoader("./Ape.pdf")
# loader = UnstructuredPDFLoader("https://github.com/Dev-Anky07/GPTBot/blob/main/Apecoin.pdf")
data = loader.load()

# Note: If you're using PyPDFLoader then it will split by page for you already
print(f'You have {len(data)} document(s) in your data')

# Note: If you're using PyPDFLoader then we'll be splitting for the 2nd time.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

# Change this to use environmental variables
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_API_ENV = os.environ['PINECONE_API_ENV']

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Initialize pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

index_name = "ape"  # Ape Assistant

docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

query = "What's AIP 239?"
docs = docsearch.similarity_search(query)

# Here's an example of the first document that was returned
print(docs[0].page_content[:450])

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

llm = OpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")

query = "What is the Ape Assembly?"
docs = docsearch.similarity_search(query)

output = chain.run(input_documents=docs, question=query)
print(output)
