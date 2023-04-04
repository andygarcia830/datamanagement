# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document

class MetaData(Document):
	pass


@frappe.whitelist()
def create_json(name):
	print('CREATE JSON CALLED')
	maindoc = frappe.get_doc('MetaData',name)
	print(f'GOT DOC {maindoc}')
	# get Steward List
	stewards = frappe.get_all('StewardList', filters = dict(parent=name),fields = 'steward')
	stewardList=[]
	for entry in stewards:
		print(f'GOT STEWARD {entry.steward}')
		stewardList.append(entry.steward)

	# get sources
	sources = frappe.get_all('MetaDataReference', filters = dict(parent=name),fields = 'metadata')
	sourceList=[]
	for entry in sources:
		print(f'GOT SOURCE {entry.metadata}')
		sourceList.append(entry.metadata)

	# get fields
	fields = frappe.get_all('MetaDataFields', filters = dict(parent=name),fields = 'name1,description,type,source')
	fieldList=[]

	for entry in fields:
		fieldDict={}
		print(f'GOT FIELD {entry.name1}')
		fieldDict['name1']=entry.name1
		fieldDict['description']=entry.description
		fieldDict['type']=entry.type
		fieldDict['source']=entry.source
		fieldList.append(fieldDict)


	jsonList = []
	jsonList.append({'name':maindoc.name1})
	jsonList.append({'description':maindoc.description})
	jsonList.append({'owner':maindoc.owner})
	jsonList.append({'steward':stewardList})
	jsonList.append({'source':sourceList})	
	jsonList.append({'fields':fieldList})	
	jsonList.append({'url':maindoc.url})
	jsonList.append({'creation_date':maindoc.creation_date})
	jsonList.append({'storage_type':maindoc.storage_type})
	jsonList.append({'retention_period_in_days':maindoc.retention_period_in_days})
	print(jsonList)
	maindoc.set('json',str(jsonList))
	maindoc.save()


@frappe.whitelist()
def fetch_source_fields(name,source):
	maindoc = frappe.get_doc('MetaData',name)
	currentFields= maindoc.fields
	print(f'NEW FIELDS {currentFields}')
	sourceJson = json.loads(source)
	#print(f'FETCHING SOURCE {source}')
	for sourceItem in sourceJson:
		print(f'GOT SOURCE {sourceItem}')
		thisName = sourceItem['metadata']
		thisDoc = frappe.get_doc('MetaData',thisName)
		
		fields = frappe.get_all('MetaDataFields', filters = dict(parent=thisName),fields = 'name1,description,type,source')
		print(f'FETCHING FIELDS {fields}')
	
		for item in fields:
			match = 0
			# check if field already exists in list
			for entry in currentFields:
				print(f'CHECKING FIELD {entry.name1} {entry.source}')
				if entry.name1 == item.name1 and entry.source == thisName:
					print(f'SKIPPING {entry.name}')
					match = 1
					
			

			if match == 0:
				print(f'FETCHING FIELD {item}')
				thisField = maindoc.append('fields',{})
				thisField.name1=item.name1
				thisField.description=item.description
				thisField.type=item.type
				thisField.source=thisName
			#newFields.append(thisField)
	#print(f'NEW FIELDS {newFields}')
	#maindoc.fields=newFields
	maindoc.save()
		
	