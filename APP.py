from flask import Flask
from flask import request, jsonify
import os
import json
import traceback
from langchain.output_parsers import StructuredOutputParser, ResponseSchema,OutputFixingParser
# from langchain.chat_models import ChatOpenAI
from function import file_loader, load_vector_store,embend_chunks
from function import query_doc
# from resumeevaluate import evaluate_resume
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain.output_parsers import OutputFixingParser
# from langchain.chat_models import ChatGroq
# import google.generativeai as genai
from langchain.chat_models import ChatOpenAI
from flask_cors import CORS



# os.environ["OPENAI_API_KEY"] = "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"  # Replace with your Groq API key
# groq_api_base = "https://api.groq.com/openai/v1"

from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file
App2 = Flask(__name__)
CORS(App2)
upload_folder= 'uploadresume'
extracted_data_storage = {}
retriever_storage = {}
os.makedirs(upload_folder, exist_ok=True)
upload_folder2='uploadqueries'
os.makedirs(upload_folder2, exist_ok=True)

'''
@App2.route('/upload',methods=['POST'])

def upload_file ():

    if 'file' not in request.files:
     return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        retriever = file_loader(file_path)
        print(f"File processing completed successfully for: {file.filename}")
        # Store the result if needed
        extracted_data_storage[file.filename] = {
            'retriever': 'created',  # Don't store the actual retriever object
            'status': 'processed'
        }
        
        return jsonify({
            "message": "File processed successfully", 
            "file": file.filename,
            "status": "success"
        }), 200
        
    except Exception as e:
        print(f"Processing failed for {file.filename}: {str(e)}")
        print(f"Full error traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500
'''
'''
@App2.route('/check_resume', methods=['POST'])
def check_resume():
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        query = data.get('query', '')

        if not resume_text or not query:
            return jsonify({'error': 'Both resume_text and query are required.'}), 400

        result = evaluate_resume(resume_text, query)

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in resume checking: {str(e)}")
        print(f"Full error traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Resume checking failed: {str(e)}'}), 500
'''
@App2.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        _, extracted_text = file_loader(file_path)
        # retriever_storage[file.filename] = retriever,
        # print(f"File processing completed successfully for: {file.filename}")
        # retriever_storage[file.filename] =retriever 
        # print("Current retriever_storage keys:", retriever_storage.keys())

        # Save extracted text in memory for this session
        extracted_data_storage[file.filename] = {
            'text': extracted_text,
            'status': 'processed',
            # 'retriever': 'created'
        }
        return jsonify({
            "message": "File processed successfully",
            "file": file.filename,
            "status": "success"
        }), 200

    except Exception as e:
        print(f"Processing failed for {file.filename}: {str(e)}")
        print(f"Full error traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500
 
# @App2.route('/resume_analyze', methods=['POST'])
# def analyze_resume():
#     try:
#         data=request.get_json()
#         file_name = data.get('file_name', '')
#         query = data.get('query', '')
#         if not file_name or not query:
#          return jsonify({'error': 'Both file_name and query are required.'}), 400
#         '''
#         if file_name not in extracted_data_storage:
#          print("Available files:", extracted_data_storage.keys())
#          print("File requested:", file_name)
#          return jsonify({'error': 'File not found or not processed yet.'}), 404
#         '''
#         # resume_text = extracted_data_storage[file_name]['text']
#         # retriever, _ = file_loader(f'uploads/{file_name}')
#         retriever, resume_text = file_loader(f'uploads/{file_name}')
#         temperature = data.get('temperature', 0.0) # Default to strict evaluation if not provided
#         llm = ChatOpenAI (model="deepseek-r1-distill-llama-70b",
#             openai_api_base=groq_api_base,openai_api_key=os.environ["OPENAI_API_KEY"],
#             temperature=temperature)
        
#         response_schemas = [
#                 ResponseSchema(name="score", description="Match score out of 10"),
#                 ResponseSchema(name="matched_keywords", description="List of matched keywords"),
#                 ResponseSchema(name="missing_keywords", description="List of missing keywords"),
#                 ResponseSchema(name="status", description="Pass, Review, or Reject"),
#                 ResponseSchema(name="explanation", description="Brief explanation of the evaluation")
#             ]

#         parser = StructuredOutputParser.from_response_schemas(response_schemas)
#         format_instructions = parser.get_format_instructions()

#         custom_prompt = PromptTemplate(
#         input_variables=["context", "question","format_instructions"],
#         template = """
#         You are an expert HR's CV/Resume analyzer who evaluates the resume data against the HR query.
#         resume following the instructions below.
#         Context (Extracted Resume Text):
#         {context}

#         Query:
#         {question}
#         Instructions:
#         1. Check if the resume matches the query based on skills, experience, and relevant keywords.
#         2. Provide a match score out of 10.
#         3. List matched keywords.
#         4. List missing keywords.
#         5. Provide a decision label: Pass (score >= 8), Review (score >= 5), Reject (score < 5).
#         6. Give a brief explanation.

#         Remove all backslash and unwanted symbols from the response.
#         {format_instructions}
#         Only return the JSON object. Do not include any other text, explanation, or reasoning outside the JSON.
#             """
#                 )
                
#         rag_chain = RetrievalQA.from_chain_type(
#                 llm=llm,
#                 retriever=retriever,
#                 chain_type="stuff",
#                 chain_type_kwargs={"prompt": custom_prompt}
#             )
#         rag_response = rag_chain.invoke(query)

#         return jsonify({
#                 "mode": "rag",
#                 "temperature": temperature,
#                 "result": rag_response
#             }), 200

#     except Exception as e:
#         print(f"Error in resume analyzer: {str(e)}")
#         print(f"Full error traceback: {traceback.format_exc()}")
#         return jsonify({'error': f'Resume analyzer failed: {str(e)}'}), 500
# To store uploaded questions globally

uploaded_queries = {}

# Load any previously saved queries from disk (JSON files)
for filename in os.listdir(upload_folder2):
    if filename.endswith('.json'):
        filepath = os.path.join(upload_folder2, filename)
        try:
            with open(filepath, 'r') as f:
                query_key = filename.replace('.json', '').strip().lower()
                uploaded_queries[query_key] = json.load(f)
        except Exception as e:
            print(f"Failed to load {filename}: {str(e)}")

@App2.route('/getquery', methods=['POST'])
def getquery():
    print("Request files:", request.files)
    print("Request form:", request.form)
    print("Request content-type:", request.content_type) 
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    queryfile_path = os.path.join(upload_folder2, file.filename)
    file.save(queryfile_path)
    print("All file keys received:", list(request.files.keys()))

    try:
        Questions = query_doc(queryfile_path)

        if not Questions:
            return jsonify({'error': 'No questions found in the file.'}), 400

        # uploaded_queries[file.filename] = Questions  # Store the questions by filename
        normalized_filename = file.filename.strip().lower()
        uploaded_queries[normalized_filename] = Questions
        print("Uploaded query stored as:", normalized_filename)
                # Save questions as a JSON file
        json_path = os.path.join(upload_folder2, f"{normalized_filename}.json")
        with open(json_path, 'w') as f:
            json.dump(Questions, f)

        print("Uploaded query stored as:", normalized_filename)

        return jsonify({
            "message": "Query file uploaded and processed successfully.",
            "file": file.filename,
            "questions": Questions
        }), 200

    except Exception as e:
        print(f"Error processing query file: {str(e)}")

        return jsonify({'error': f'Failed to process query file: {str(e)}'}), 500
# main resume_analyze start

@App2.route('/resume_analyze', methods=['POST'])
def analyze_resume():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error' : 'invalid or missing json in it' }),200
        query_file = data.get('query_file', '')
        if query_file == '' or query_file not in uploaded_queries:
          return jsonify({
           'error': f"Query file '{query_file}' not found.",
           'available_query_files': list(uploaded_queries.keys()) }), 400
        print("Request data:", request.data)
        print("Request content-type:", request.content_type)
        print("Uploaded queries:", list(uploaded_queries.keys()))
        print("Requested query_file:", query_file)

        # retriever, resume_text = file_loader(f'uploads/{file_name}')
        embedding_function = embend_chunks()
        retriever = load_vector_store(embedding_function)

        # retriever = load_vector_store(embedding_function)
        print(f"Embedding function: {embedding_function.__class__.__name__}")
        print(f"Retriever: {retriever}")

        # retriever = load_vector_store()
        # resume_text = extracted_data_storage[file_name]['text']
        Question = uploaded_queries[query_file]
        # groq_api_key = os.getenv("OPENAI_API_KEY")
        # groq_api_base = "https://api.groq.com/openai/v1"
        # llm = ChatGroq(
        #     model="gemma2-9b-it",
        #     openai_api_base=groq_api_base,
        #     openai_api_key=os.environ["OPENAI_API_KEY"],
        #     temperature=0.2 )
        # genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        # from langchain_google_genai import ChatGoogleGenerativeAI
        # llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ["GOOGLE_API_KEY"],temperature=0.6)
        llm = ChatOpenAI(
    openai_api_key=os.environ["TOGETHER_API_KEY"],
    openai_api_base="https://api.together.xyz/v1",
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",  # or any other Together-supported model
    temperature=0.2
)
        # Define expected JSON format
        response_schemas = [
            ResponseSchema(name="score", description="Match score out of 10"),
            ResponseSchema(name="matched_keywords", description="List of matched keywords"),
            ResponseSchema(name="missing_keywords", description="List of missing keywords"),
            ResponseSchema(name="status", description="Pass, Review, or Reject"),
            ResponseSchema(name="explanation", description="Brief explanation of the evaluation")
        ]

        parser = StructuredOutputParser.from_response_schemas(response_schemas)
        # format_instructions = parser.get_format_instructions()
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

        # Build the prompt
        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are an expert HR's CV/Resume analyzer who evaluates the resume data against the HR's query.

            Context (Extracted Resume Text):
            {context}

            Query:
            {question}

            Instructions:
            1. Check if the resume matches the query based on skills, experience, and relevant keywords.
            2. Provide a match score out of 10.
            3. List matched keywords.
            4. List missing keywords.
            5. Provide a decision label: Pass (score >= 8), Review (score >= 5), Reject (score < 5).
            6. Give a brief explanation.

            Only return the JSON object. Do not include any other text.
            """
        )

        # llm_chain = LLMChain(llm=llm, prompt=custom_prompt)
        # fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        rag_chain =  RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt":custom_prompt}
        )
        # response = rag_chain.invoke({
        #     "query": query
        # })
        # llm_output = response['text']
        # Parse the LLM response
        # try:
        #     parsed_response = fixing_parser.parse(llm_output)
        # except Exception as e:
        #     print("Parser failed. Raw output was:", llm_output)
        #     return jsonify({'error': f'Parsing failed: {str(e)}', 'raw_output': llm_output}), 500
        # response = rag_chain.invoke({
        #     "questions": query
        #     # "context": resume_text,  
        #     # "format_instructions": format_instructions
        # })
        # return jsonify({
        # # "mode": "llm_chain",
        # # "temperature": temperature,
        # "result": response}), 200

    #     response = rag_chain.invoke({"query": query})
    #     llm_output=response['result']
    #     try:
    #         parsed_response = fixing_parser.parse(llm_output)
    #     except Exception as e:
    #         print("Parsing failed. Raw output was:", llm_output)
    #         return jsonify({'error': f'Parsing failed: {str(e)}', 'raw_output': llm_output}), 500

    #     return jsonify({
    #         "result": parsed_response
    #     }), 200

    # except Exception as e:
    #     print(f"Error in resume analyzer: {str(e)}")
    #     print(f"Full error traceback: {traceback.format_exc()}")
    #     return jsonify({'error': f'Resume analyzer failed: {str(e)}'}), 500


        all_results = []
        approved_emails = []
        for query in Question:
         response = rag_chain.invoke({"query": query})
         llm_output = response['result']

         try:
                  parsed_response = fixing_parser.parse(llm_output)
                  all_results.append({
                    "query": query,
                     "response": parsed_response
                 })
         except Exception as e:
                    all_results.append({
                      "query": query,
                      "error": f'Parsing failed: {str(e)}',
                      "raw_output": llm_output
                })
         def parse_score(score_str):
            try:
                return float(score_str)
            except ValueError:
                if isinstance(score_str, str) and '/' in score_str:
                    try:
                        numerator, denominator = score_str.split('/')
                        return float(numerator) / float(denominator) * 10  # scale to out of 10
                    except Exception as e:
                         print(f"Failed to parse fractional score: {score_str} -> {e}")
                         print(f"Score parsing failed for: {score_str}")
            return None

        #  scores = [float(res["response"]["score"]) for res in all_results if "response" in res and "score" in res["response"]]
        scores = [
    parse_score(res["response"]["score"])
    for res in all_results
    if "response" in res and "score" in res["response"]
]

# Filter out None values (failed parses)
        scores = [s for s in scores if s is not None]

        if scores:
            total = sum(scores)
            averagescore = total / len(scores)
        
        else:
            averagescore = None
    #     if scores:
    #      total = sum(scores)
    #      average = total / len(scores)

    # # Find emails of resumes that scored > 7
    #      for res in all_results:
    #       if "response" in res and "score" in res["response"]:
    #         try:
    #             score = float(res["response"]["score"])
    #             if score > 7:
    #                 email = extracted_data_storage.get(data.get("file_name", ""), {}).get("email")
    #                 if email:
    #                     approved_emails.append(email)
    #                     print(approved_emails)
                
    #         except ValueError:
    #             continue
    #     else:
    #         average = None
    

        return jsonify({
          "results": all_results,
          "average": averagescore
          }), 200

    # except Exception as e:
    #     print(f"Error in resume analyzer: {str(e)}")
    #     print(f"Full error traceback: {traceback.format_exc()}")
    #     return jsonify({'error': f'Resume analyzer failed: {str(e)}'}), 500
    
    
        # try:
        #     parsed_response = fixing_parser.parse(llm_output)
        #         except Exception as e:
        #     print("Parsing failed. Raw output was:", llm_output)
        #     return jsonify({'error': f'Parsing failed: {str(e)}', 'raw_output': llm_output}), 500

        # return jsonify({
        #     "result": parsed_response
        # }), 200

    except Exception as e:
        print(f"Error in resume analyzer: {str(e)}")
        print(f"Full error traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Resume analyzer failed: {str(e)}'}), 500

# main resume_analyze ends 



'''
@App2.route('/result', methods=['GET'])
def get():
    return {"data": list(extracted_data_storage.values())}, 200
    # return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
'''
@App2.route('/result', methods=['GET'])
def get_processed_files():
    try:
        result = []

        for file_name, data in extracted_data_storage.items():
            result.append({
                "file_name": file_name,
                "status": data.get('status', 'unknown')
                # You can also return 'text' here if you want
            })

        return jsonify({"data": result}), 200

    except Exception as e:
        print(f"Error in get_processed_files: {str(e)}")
        return jsonify({'error': f'Failed to fetch results: {str(e)}'}), 500

if __name__ == '__main__':
    App2.run(debug=True,port=8000)