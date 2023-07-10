## Abstract :

This repo contains the codebase for as well as the contextual information (in form of a pdf) which powers the AI assistant used by the Apecoin DAO among others.

ape.py and hehe.py are using the same script but with different api keys to access different vector databases and respond to different questions asked.

Currently both are using the same keys cause there was an issue with authorisation using key2 due to a rate limit which was imposed on it.

We've decided to withold bot.py and mock.py ntil further notice casue the discord client wasn't working with this.

## Context :

This repository first loads a pdf containing contextual information, then splits it up into manageable chunks, then those split up and embeddings are created for these using OpenAI

These embeddings are used to cluster these together according to similarity and are then stored in a vector database (Pinecone in our case) which passes on the relevant data everytime there's a query

Instead od passing all the information along which is impossible due to token limitations (4000 for GPT 3.5) and even if it were possible, it wouldn'tve been efficient not to mention would be cost prohibitive.

Instead, it runs a similarity search using the Cosine parameter to identify which chunks contain useful information for the query and passes it to the model.

## Install required Dependencies :

```
pip3 install langchain
pip3 install pypdf
pip3 install pinecone-client
pip3 install openai
pip3 install tiktoken
pip3 install unstructured

```
## Configure Variables :

```
loader = PyPDFLoader("./Ape.pdf")
```
This was in the same directory, change the relative file path accordingly

```
index_name = "ape"  # Name of your Pinecone Index where you've stored vector data.
```

## Set Snvironment variables :

Get your Pinecoin API from here -> https://app.pinecone.io/organizations

Get your Open AI API form here -> https://platform.openai.com/account/api-keys

## Ask questions and hit run :

Make changes to this snippet and run. It'll give out an appropriate answer for the query you jst made and all you'll be left with would be awe for modern technology.

```
query = "What is the overall Cost of AIP 239 : Governance Working group ?"
docs = docsearch.similarity_search(query)

output = chain.run(input_documents=docs, question=query)
print(output)
```

Voila ! you're all set 😉