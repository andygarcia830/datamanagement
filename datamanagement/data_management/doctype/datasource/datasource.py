# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3,json
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
		tableEntry={}
		tableEntry['table_name']=item.table_name
		partitions = json.loads(item.partitions)
		tableEntry['paritions']=partitions
		tableEntry['table_type']=item.table_type
		tableEntry['last_processed_id']=item.last_processed_id
		
		tables.append(tableEntry)
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


	result.append({'connectionType':maindoc.connection_type})
	result.append({'sshHost':maindoc.ssh_tunnel_host})
	result.append({'sshPort':maindoc.ssh_tunnel_port})
	result.append({'sshLogin':maindoc.ssh_tunnel_login})
	result.append({'sshPassword':maindoc.ssh_tunnel_password})	
	result.append({'sshPEMPath':maindoc.ssh_tunnel_pem_path})	
	result.append({'localPort':maindoc.local_port})	
	result.append({'remotePort':maindoc.remote_destination_port})	

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


@frappe.whitelist()
def set_last_processed_id(datasource, table, value):
	maindoc = frappe.get_doc('DataSource',datasource)

	for item in maindoc.tables:
		if item.table_name == table:
			item.last_processed_id=value
			maindoc.save()
			return 'SUCCESS'
		
	frappe.throw(f'Table {table} does not exist in Data Source {datasource}')


