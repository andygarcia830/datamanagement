# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document

class DataMapping(Document):
	pass


@frappe.whitelist()
def fetch_values(metadata,name):
	print(f'FETCHING DATA FOR {metadata} {name}')
	metadatadoc=frappe.get_doc('MetaData',metadata)
	result = {}
	if metadatadoc!=None:
		result['description']=metadatadoc.description
		result['source']=metadatadoc.source
		result['fields']=metadatadoc.fields
		result['url']=metadatadoc.url
		result['storage_type']=metadatadoc.storage_type
		result['creation_date']=metadatadoc.creation_date
		result['retention_period_units']=metadatadoc.retention_period_units
		result['retention_period_value']=metadatadoc.retention_period_value
		

	return result


@frappe.whitelist()
def fetch_fields(metadata,name):
	print(f'FETCHING FIELDS FOR {metadata} {name}')
	metadatadoc=frappe.get_doc('MetaData',metadata)
	result = []
	for item in metadatadoc.fields:
		result.append(item.name1)

	print(result)
	return result



@frappe.whitelist()
def fetch_origin_fields(sources):
	print(f'FETCHING ORIGIN FIELDS FOR {sources}')
	fields = json.loads(sources)
	result=[]
	for item in fields:
		metadata = item['metadata']
		mddoc=frappe.get_doc('MetaData',metadata)
		mdfields = mddoc.fields
		# combine MetaData and Field Name
		for item2 in mdfields:
			thisEntry=metadata+':'+item2.name1
			result.append(thisEntry)

		#print(metadata)
	return result