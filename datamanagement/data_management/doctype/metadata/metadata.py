# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document

class MetaData(Document):
	pass


@frappe.whitelist()
def create_json(name):
	#print('CREATE JSON CALLED')
	maindoc = frappe.get_doc('MetaData',name)
	#print(f'GOT DOC {maindoc}')
	# get Steward List
	stewards = frappe.get_all('StewardList', filters = dict(parent=name),fields = 'steward')
	stewardList=[]
	for entry in stewards:
		#print(f'GOT STEWARD {entry.steward}')
		stewardList.append(entry.steward)

	# get sources
	sources = frappe.get_all('MetaDataReference', filters = dict(parent=name),fields = 'metadata')
	sourceList=[]
	for entry in sources:
		#print(f'GOT SOURCE {entry.metadata}')
		if sourceList.count(entry.metadata) == 0:
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
		fieldDict['origin']=entry.origin
		if fieldList.count(fieldDict) == 0:
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
	jsonList.append({'retention_period_units':maindoc.retention_period_units})
	jsonList.append({'retention_period_value':maindoc.retention_period_value})
	#print(jsonList)
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
		
		fields = frappe.get_all('MetaDataFields', filters = dict(parent=thisName),fields = 'name1,description,type,source,origin')
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
				#print(f'FETCHING FIELD {item}')
				thisField = maindoc.append('fields',{})
				thisField.name1=item.name1
				thisField.description=item.description
				thisField.type=item.type
				thisField.source=thisName
				#print(f'ITEM ORIGIN= {item.origin}')
				if item.origin == None or len(item.origin) == 0:
					thisField.origin = thisName
				else:
					thisField.origin = item.origin
			#newFields.append(thisField)
	#print(f'NEW FIELDS {newFields}')
	#maindoc.fields=newFields
	maindoc.save()
		
@frappe.whitelist()
def set_origin(doc):
	maindoc = frappe.get_doc('MetaData',doc)
	print('SET ORIGIN CALLED')
	fields = maindoc.fields
	for item in fields:
		print(f'THIS FIELD={item.origin}')

		if item.origin == None or item.origin=='':
			item.origin=maindoc.name
			print(f'SETTING ORIGIN TO {maindoc.name}')
		
		if item.source == None or item.source=='':
			item.source=maindoc.name
	maindoc.save()

	print(f'FIELDS={fields}')


@frappe.whitelist()
def validate_sources(doc):
	fields = json.loads(doc)
	for item in fields:
		print(item)
	
		if item['name1'] != None and item['name1'] != '':
			name1=item['name1']
			print(f'THIS FIELD={name1}')
			validated = False

			try:

				if item['source'] == None or item['source'] == '':
					validated = True
			except:
				validated = True

			else:
				source = item['source']
				thisMD2=frappe.get_doc('MetaData',source)
				for item2 in thisMD2.fields:
					if item2.name1 == name1:
						validated = True

			if not validated:
				msg= f'Field {name1} does not exist in Source {source}'
				return msg
			try:
				origin=item['origin']
				if (origin == None or origin == '' or source == origin):
					pass
				else:
					thisMD3=frappe.get_doc('MetaData',item['origin'])
					for item3 in thisMD3.fields:
						if item3.name1 == name1:
							validated = True
					if not validated:
						msg= f'Field {name1} does not exist in Origin {origin}'
						return msg


			except:
				validated = True
			
			

@frappe.whitelist()
def fetch_tables(name):
	maindoc = frappe.get_doc('MetaData',name)
	datasource =  frappe.get_doc('DataSource',maindoc.datasource)
	tables = datasource.tables
	result=[]
	for item in tables:
		result.append(item.table_name)

	return result
