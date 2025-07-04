from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.document_loaders.csv_loader import CSVLoader


persist_directory = "./chroma_db"
collection_name = "resume_analysis" 



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
        print("Embeddings initialized")

        retriever = vector_store1(embedding_function, split_docs)
        print("Retriever and vector store created successfully")
        # retriever = vector_store1(embedding_function, split_docs, resume_filename=os.path.basename(file_path))


        return retriever, extracted_text

    except Exception as e:
        print(f"Error in file_loader: {str(e)}")
        raise e



def chunk_extracteddata(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)

def embend_chunks():
         return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

   
       



def vector_store1(embedding_function, split_docs):
    print(f"Using embedding function: {embedding_function.__class__.__name__}")

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_function,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    vectorstore.persist()
    return vectorstore.as_retriever(embedding_function=embedding_function)
# def vector_store1(embedding_function, split_docs, resume_filename=None):
#     print(f"Using embedding function: {embedding_function.__class__.__name__}")

#     # Inject metadata: resume_id for filtering later
#     metadatas = [{"resume_id": resume_filename}] * len(split_docs)

#     vectorstore = Chroma.from_documents(
#         documents=split_docs,
#         embedding=embedding_function,
#         persist_directory=persist_directory,
#         collection_name=collection_name,
#         metadatas=metadatas
#     )
#     vectorstore.persist()
#     return vectorstore.as_retriever(search_kwargs={"filter": {"resume_id": resume_filename}})




# def load_vector_store(embedding_function):
#     vectorstore = Chroma(
#         persist_directory=persist_directory,
#         embedding=embedding_function,
#         collection_name=collection_name
#     )
#     return vectorstore.as_retriever()
def load_vector_store(embedding_function=None):
    if embedding_function is None:
        embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function,
        collection_name=collection_name
    )

    return vectorstore.as_retriever()

# def load_vector_store(resume_filename, embedding_function=None):
#     if embedding_function is None:
#         embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     vectorstore = Chroma(
#         persist_directory=persist_directory,
#         embedding_function=embedding_function,
#         collection_name=collection_name
#     )

#     # Add filtering based on filename
#     return vectorstore.as_retriever(search_kwargs={"filter": {"resume_id": resume_filename}})



    # But you still need the embedding_function when querying (handled internally)
    # return vectorstore.as_retriever(embedding_function=embedding_function)



def query_doc(queryfile_path):
    try:
        loader = CSVLoader(file_path=queryfile_path)
        query_documents = loader.load()
        return [doc.page_content for doc in query_documents]
    except Exception as e:
        print(f"Error while loading CSV: {e}")
        return []
