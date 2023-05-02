# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document
from frappe.utils import get_site_name

from langchain.llms import OpenAI
from langchain.chat_models.openai import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader


from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores.faiss import FAISS


from langchain.embeddings import OpenAIEmbeddings

from langchain.prompts.prompt import PromptTemplate,StringPromptTemplate
from langchain.chains import ChatVectorDBChain

from langchain.agents import Tool
from langchain.agents import initialize_agent
#from langchain.agents import create_sql_agent
import pandas as pd

from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor

from datamanagement.data_management.doctype.chat_gpt.sql_with_memory import create_sql_agent, create_sql_agent_with_memory


from typing import List, Union

import os,pickle

from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext



class ChatGPT(Document):
	pass



def api_key():
    try:
        if (os.environ["OPENAI_API_KEY"] == None or os.environ["OPENAI_API_KEY"] == ''):
            os.environ["OPENAI_API_KEY"] = frappe.get_doc('OpenAI Settings').openai_api_key
            
    except:
        os.environ["OPENAI_API_KEY"] = frappe.get_doc('OpenAI Settings').openai_api_key


    
    key=os.environ["OPENAI_API_KEY"]
    print(f'OPENAI KEY={key}')


@frappe.whitelist()
def send(msg,jsonStr):
	print(f'MSG {msg}')
	print(f'JSON {jsonStr}')
	jsonDict=json.loads(jsonStr)
	jsonDict.append({"input":msg})
	jsonDict.append({"output":chat_gptbot(msg)})
	return jsonDict



# 



def get_chain(vectorstore,prompt):
    api_key()
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
    You can assume the question about the candidate list.
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

    template = prompt+"""
    Question: {question}
    =========
    {context}
    =========
    Answer in Markdown:"""
    QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])


    chain_type_kwargs = {"prompt": QA_PROMPT}
    llm = OpenAI(temperature=0.2,max_tokens=2048)
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )

    #qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever(), chain_type_kwargs=chain_type_kwargs)

    return qa_chain


# def answer_with_embeddings(msg,jsonStr):
#     vector_dir='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_vectors/'+contextdoc.csv_directory
#     # with open(vector_file, "rb") as f:
#     #     vectorstore = pickle.load(f)
#     embeddings = OpenAIEmbeddings()
#     vectorstore=FAISS.load_local(vector_dir,embeddings)
#     prompt = contextdoc.instructions_prompt
#     if prompt == None:
#         prompt = ''
#     qa_chain = get_chain(vectorstore,prompt)
#     jsonDict=json.loads(jsonStr)
#     #print(jsonDict)
#     print(vectorstore)
#     result = qa_chain({"question": msg, "chat_history": jsonDict})
#     jsonDict.append((msg,result['answer']))
#     print(f"ANSWER:{result['answer']}")
#     return jsonDict



@frappe.whitelist()
def ask_question(msg,jsonStr,context):
    api_key()
    contextdoc=frappe.get_doc('GPT Context',context)
    if (contextdoc != None):
        #return answer_with_embeddings(msg,jsonStr)
        datasource = frappe.get_doc('DataSource',contextdoc.data_source)
        connectstring=f'{datasource.sql_type}://{datasource.db_username}:{datasource.db_password}@{datasource.host}:{datasource.port}/{datasource.database_name}'
        print(f'CONNECTING WITH {connectstring}')
        return answer_with_sql_agent(msg,jsonStr,connectstring)

        # csv_file='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_training/candidates/candidates-2023-04-14.csv'
        # return answer_with_pandas_agent(msg,jsonStr,csv_file)


        


# @frappe.whitelist()
# def train_chatbot(context):
#     api_key()
#     contextdoc=frappe.get_doc('GPT Context',context)
#     if (contextdoc != None):
#         vector_directory='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_vectors/'+contextdoc.csv_directory
#         csv_directory='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_training/'+contextdoc.csv_directory
#         load_csv(csv_directory,vector_directory)
  
@frappe.whitelist()
def fetch_greeting(context):
    contextdoc=frappe.get_doc('GPT Context',context)
    if (contextdoc != None):
        return contextdoc.greeting_message
  


# Using the SQL Agent Approach
def answer_with_sql_agent(msg,jsonStr,connectstring):
    api_key()
    jsonDict=json.loads(jsonStr)

    
    db = SQLDatabase.from_uri(connectstring)
    toolkit = SQLDatabaseToolkit(db=db)

    #print(f'TOOLS={toolkit.get_tools()}')


    # agent_executor = initialize_agent(

    #     agent='conversational-react-description',
    #     tools=toolkit.get_tools(),
    #     llm = OpenAI(temperature=0,max_tokens=2048),
    #     verbose=True,
    #     memory=memory,
    #     max_iterations=10
    # )

    
    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0,model_name='text-davinci-003'),
        #llm=ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo'),
        toolkit=toolkit,
        verbose=True,
    )
    if jsonStr == None:
         jsonStr=''

    print(f'CHAT HISTORY={jsonStr}')

    result = agent_executor.run({'input':msg,'chat_history':jsonStr})
    #print(f'RESULT={result}')
    jsonDict.append((msg,result))
    return jsonDict

# Using the Pandas Agent approach
def answer_with_pandas_agent(msg,jsonStr,csv_file):
    api_key()
    jsonDict=json.loads(jsonStr)

    
    df = pd.read_csv(csv_file)
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0,model_name='text-davinci-003'), df, verbose=True)

 

    result = agent.run(msg)
    #print(f'RESULT={result}')
    jsonDict.append((msg,result))
    return jsonDict




# def chat_gptbot(input_text):
#     index_file='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_index.json'
#     print(f'GPT index file={index_file}')
#     index = GPTSimpleVectorIndex.load_from_disk(index_file)
#     response = index.query(input_text, response_mode="compact")
#     return response.response




# def construct_index(directory_path):
#     index_file='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_index.json'
#     print(f'GPT index file={index_file}')
#     max_input_size = 4096
#     num_outputs = 512
#     max_chunk_overlap = 20
#     chunk_size_limit = 600

#     prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

#     llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

#     documents = SimpleDirectoryReader(directory_path).load_data()
    
#     service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)


#     index =  GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

#     index.save_to_disk(index_file)

    #return index


#def load_csv(csv_folder,vector_directory):
#     api_key()

#     documents=[]
#     vectorstore=None

#     for filename in os.listdir(csv_folder):
#         file = os.path.join(csv_folder, filename)
#         # checking if it is a file
        
#         if  filename.endswith('.csv') and os.path.isfile(file):
#             print(f'adding {file} to training data')
#             loader = CSVLoader(file_path=file)
#             data = loader.load()
#             # Split text
#             text_splitter = RecursiveCharacterTextSplitter(  chunk_size = 100,
#                 chunk_overlap  = 20,
#                 length_function = len,)
#             documents = text_splitter.split_documents(data)
#             print(f'DOCUMENTS SIZE={len(documents)}')
#             # Load Data to vectorstore
#             embeddings = OpenAIEmbeddings()
#             if vectorstore == None:
#                 vectorstore = FAISS.from_documents(documents, embeddings)
#                 print(f'VECTOR STORE SIZE={vectorstore}')
#             else:
#                 thisvector = FAISS.from_documents(documents, embeddings)
#                 vectorstore.merge_from(thisvector)

#     print(f'SAVING TO {vector_directory}: {vectorstore}')
#     # Save vectorstore
#     # with open(vector_file, "wb") as f:
#     #     pickle.dump(vectorstore, f)
#     vectorstore.save_local(vector_directory)
