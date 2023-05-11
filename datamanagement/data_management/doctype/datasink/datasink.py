# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

# import frappe
# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3,json
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
from frappe.model.document import Document

class DataSink(Document):
	pass


@frappe.whitelist()
def fetch_details(datasink):
	maindoc=frappe.get_doc('DataSink',datasink)
	if maindoc == None:
		frappe.throw(f'Requested datasink {datasink} not found')
	
	result={}
	result['method']=maindoc.method
	result['sqlType']=maindoc.sql_type
	result['clientName']=frappe.get_doc('Client Configuration').client_namespace
	result['hostName']=maindoc.host
	result['portNo']=maindoc.port
	result['dbName']=maindoc.database_name
	result['schemaName']=maindoc.schema_name

	result['table']=maindoc.table
	result['usr']=maindoc.db_username
	result['pwd']=maindoc.db_password
	#result['processDate']=maindoc.process_date


	result['connectionType']=maindoc.connection_type
	result['sshHost']=maindoc.ssh_tunnel_host
	result['sshPort']=maindoc.ssh_tunnel_port
	result['sshLogin']=maindoc.ssh_tunnel_login
	result['sshPassword']=maindoc.ssh_tunnel_password	
	result['sshPEMPath']=maindoc.ssh_tunnel_pem_path	
	result['localPort']=maindoc.local_port	
	result['remoteHost']=maindoc.remote_destination_host	
	result['remotePort']=maindoc.remote_destination_port	

	result['bucketName']=maindoc.bucket_name

	return result




@frappe.whitelist()
def set_last_processed_id(datasink, table, value):
	maindoc = frappe.get_doc('Datasink',datasink)

	for item in maindoc.tables:
		if item.table_name == table:
			item.last_processed_id=value
			maindoc.save()
			return 'SUCCESS'
		
	frappe.throw(f'Table {table} does not exist in Data Source {datasink}')


