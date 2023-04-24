# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
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
	result.append({'sqlType':maindoc.sql_type})
	result.append({'clientName':frappe.get_doc('Client Configuration').client_namespace})
	result.append({'hostName':maindoc.host})
	result.append({'portNo':maindoc.port})
	result.append({'dbName':maindoc.database_name})
	result.append({'schemaName':maindoc.schema_name})
	result.append({'tables':tables})
	result.append({'usr':maindoc.db_username})
	result.append({'pwd':maindoc.db_password})
	result.append({'processDate':maindoc.process_date})
	result.append({'bucketName':maindoc.bucket_name})

	return result



@frappe.whitelist()
def create_folders(name):
	print('CREATE')
	maindoc = frappe.get_doc('DataSource',name)
	storage_type=maindoc.target_storage_type
	resource=frappe.get_doc('Client Configuration').bucket_name
	folder=maindoc.database_name

	tables = []
	for item in maindoc.tables:
		tables.append(item.table_name)

	print(f'storage={storage_type} folder={folder} tables={tables}')

	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3.put_object(Bucket=resource,Key=folder)

		for item in tables:
			thisObject=folder+'/'+item
			s3.put_object(Bucket=resource,Key=thisObject)


