# from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader

# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document

persist_directory = "./chroma_db"
# function to load the pdf

def file_loader(file_path):
    print("Starting file_loader...")

    try:
        loader = PyPDFLoader(file_path)
        print("PDF loader initialized")

        docs = loader.load()
        print("PDF loaded successfully")

        extracted_text = " ".join([doc.page_content for doc in docs])
        print("Text extracted successfully")

        split_docs = chunk_extracteddata(docs)
        print("Text split into chunks successfully")

        embedding_function = embend_chunks()
        print("Embeddings created successfully")

        retriever = vector_store1(embedding_function, split_docs)

        # retriever = retriever_return(vectorstore)
        # print("Retriever created successfully")

        return retriever,extracted_text

    except Exception as e:
        print(f"Error in file_loader: {str(e)}")
        raise e

#function to create chunks of the pdf
def chunk_extracteddata(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # docs = [Document(page_content='extracted_text')]
    split_docs = text_splitter.split_documents(docs)
    return split_docs

#function to create embeddings from the chunks
def embend_chunks():
    #embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embedding_function

# function to vectorstore the embedded chunks
# def vector_store1(embedding_function,split_docs):
#     vectorstore=Chroma.from_documents(documents=split_docs, embedding= embedding_function)
#     retriever= vectorstore.as_retriever()
#     print("Retriever created successfully")
#     return retriever
'''
def vector_store1(embedding_function, split_docs):
    try:
        from langchain_community.vectorstores import FAISS
        print(f"Creating FAISS vector store with {len(split_docs)} documents...")
        
        vectorstore = FAISS.from_documents(
            documents=split_docs, 
            embedding=embedding_function
        )
        print("FAISS vector store created successfully")
        
        retriever = vectorstore.as_retriever()
        print("FAISS retriever created successfully")
        return retriever
        
    except Exception as e:
        print(f"Error in FAISS vector_store1: {str(e)}")
        raise e
'''
from langchain_community.vectorstores import Chroma

def vector_store1(embedding_function, split_docs):
    persist_directory = "./chroma_db"  # You can change this to any path you prefer
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    vectorstore.persist()  # This will save the vector store to disk
    retriever = vectorstore.as_retriever()
    print("Retriever created and vector store saved successfully")
    return retriever
def load_vector_store():
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    retriever = vectorstore.as_retriever()
    print("Vector store loaded successfully from disk.")
    return retriever
def query_doc(qureyfile_path):
    try:
        loader = CSVLoader(file_path=qureyfile_path)
        qureydocuments = loader.load()
        questions = [doc.page_content for doc in qureydocuments]
        return questions
    except Exception as e:
        print(f"Error while loading CSV: {e}")
        return []


