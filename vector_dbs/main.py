import os
from re import template

from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import  create_retrieval_chain

if __name__ == "__main__":
    print("Retrieving")

    embedder = OpenAIEmbeddings()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    query = "What is Pinecone in Machine Learning?"
    #chain = PromptTemplate.from_template(template=query) | llm

    vectorstore = PineconeVectorStore(
        index_name=os.getenv("INDEX_NAME"), embedding=embedder
    )

    retrieval_qa_chat_prompt = hub.pull("rag-prompts-gn/retrieval-qa-chat-gn")
    #print(retrieval_qa_chat_prompt)

    template = """
        Use the following pieces of context to answer the question at the end. If you dont 
        know the answer, just say I don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer concise as possible. 
        Always say, "thanks for asking" at the end of the answer. 
        
        {context}
        
        Question: {question}
        
        Helpful Answer:
    """
    new_rag_prompt = PromptTemplate.from_template(template=template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | new_rag_prompt
        | llm
    )

    res = rag_chain.invoke(query).content
    print(res)

    #combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    #retrieval_chain = create_retrieval_chain(
    #    retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    #)

    #result = retrieval_chain.invoke({
    #    "input": query,
    #    "chat_history": [],  # or previous chat history if you have
    #})

    #print(result)