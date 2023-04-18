# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DataSource(Document):
	pass


@frappe.whitelist()
def fetch_details(datasource):
	maindoc=frappe.get_doc('DataSource',datasource)
	if maindoc == None:
		frappe.throw(f'Requested datasource {datasource} not found')
	
	tables = []
	for item in maindoc.tables:
		tables.append(item.table_name)
	print(f'TABLES={tables}')
	result=[]
	result.append({'method':maindoc.method})
	result.append({'sqlType':maindoc.type})
	result.append({'clientName':frappe.get_doc('Client Configuration').client_namespace})
	result.append({'hostName':maindoc.host})
	result.append({'portNo':maindoc.port})
	result.append({'dbName':maindoc.database_name})
	result.append({'schemaName':maindoc.schema_name})
	result.append({'tables':tables})
	result.append({'usr':maindoc.db_username})
	result.append({'pwd':maindoc.db_password})
	result.append({'processDate':maindoc.process_date})

	return result
