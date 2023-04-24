# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document
from frappe.utils import get_site_name

from langchain.llms import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader


from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores.faiss import FAISS


from langchain.embeddings import OpenAIEmbeddings

from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ChatVectorDBChain

from langchain.chains import RetrievalQA

import os,pickle

from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext



class ChatGPT(Document):
	pass


def api_key():
    try:
        os.environ["OPENAI_API_KEY"] 
        
    except:
        os.environ["OPENAI_API_KEY"] = frappe.get_doc('OpenAI Settings').openai_api_key


@frappe.whitelist()
def send(msg,jsonStr):
	print(f'MSG {msg}')
	print(f'JSON {jsonStr}')
	jsonDict=json.loads(jsonStr)
	jsonDict.append({"input":msg})
	jsonDict.append({"output":chat_gptbot(msg)})
	return jsonDict



def load_csv(csv_folder,vector_directory):
    api_key()

    documents=[]
    vectorstore=None

    for filename in os.listdir(csv_folder):
        file = os.path.join(csv_folder, filename)
        # checking if it is a file
        
        if  filename.endswith('.csv') and os.path.isfile(file):
            print(f'adding {file} to training data')
            loader = CSVLoader(file_path=file)
            data = loader.load()
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(  chunk_size = 100,
                chunk_overlap  = 20,
                length_function = len,)
            documents = text_splitter.split_documents(data)
            print(f'DOCUMENTS SIZE={len(documents)}')
            # Load Data to vectorstore
            embeddings = OpenAIEmbeddings()
            if vectorstore == None:
                vectorstore = FAISS.from_documents(documents, embeddings)
                print(f'VECTOR STORE SIZE={vectorstore}')
            else:
                thisvector = FAISS.from_documents(documents, embeddings)
                vectorstore.merge_from(thisvector)

    print(f'SAVING TO {vector_directory}: {vectorstore}')
    # Save vectorstore
    # with open(vector_file, "wb") as f:
    #     pickle.dump(vectorstore, f)
    vectorstore.save_local(vector_directory)




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

@frappe.whitelist()
def ask_question(msg,jsonStr,context):
    api_key()
    contextdoc=frappe.get_doc('GPT Context',context)
    if (contextdoc != None):
        vector_dir='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_vectors/'+contextdoc.csv_directory
        # with open(vector_file, "rb") as f:
        #     vectorstore = pickle.load(f)
        embeddings = OpenAIEmbeddings()
        vectorstore=FAISS.load_local(vector_dir,embeddings)
        prompt = contextdoc.instructions_prompt
        if prompt == None:
            prompt = ''
        qa_chain = get_chain(vectorstore,prompt)
        jsonDict=json.loads(jsonStr)
        #print(jsonDict)
        print(vectorstore)
        result = qa_chain({"question": msg, "chat_history": jsonDict})
        jsonDict.append((msg,result['answer']))
        print(f"ANSWER:{result['answer']}")
        return jsonDict


@frappe.whitelist()
def train_chatbot(context):
    api_key()
    contextdoc=frappe.get_doc('GPT Context',context)
    if (contextdoc != None):
        vector_directory='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_vectors/'+contextdoc.csv_directory
        csv_directory='./'+get_site_name(frappe.local.request.host)+'/private/files/gpt_training/'+contextdoc.csv_directory
        load_csv(csv_directory,vector_directory)
  
@frappe.whitelist()
def fetch_greeting(context):
    contextdoc=frappe.get_doc('GPT Context',context)
    if (contextdoc != None):
        return contextdoc.greeting_message
  




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