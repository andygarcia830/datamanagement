# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document

from langchain.llms import OpenAI
import os

from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext



class Chat(Document):
	pass


@frappe.whitelist()
def send(msg,jsonStr):
	print(f'MSG {msg}')
	print(f'JSON {jsonStr}')
	jsonDict=json.loads(jsonStr)
	jsonDict.append({"input":msg})
	jsonDict.append({"output":chatbot(msg)})
	return jsonDict





os.environ["OPENAI_API_KEY"] = "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"

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)


    index =  GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

# iface = gr.Interface(fn=chatbot,
#                      inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
#                      outputs="text",
#                      title="Andy's Custom-trained AI Chatbot")

#index = construct_index("/home/andy/Work/OpenAI/LangChain/docs")
#index = construct_index("/home/andy/frappe-bench/apps/aianalytics/aianalytics/fixtures")
#iface.launch(share=True)

#print(chatbot('Hello'))