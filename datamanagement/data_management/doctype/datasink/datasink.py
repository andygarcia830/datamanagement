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
	
	result=[]
	result.append({'method':maindoc.method})
	result.append({'sqlType':maindoc.sql_type})
	result.append({'clientName':frappe.get_doc('Client Configuration').client_namespace})
	result.append({'hostName':maindoc.host})
	result.append({'portNo':maindoc.port})
	result.append({'dbName':maindoc.database_name})
	result.append({'schemaName':maindoc.schema_name})

	result.append({'table':maindoc.table})
	result.append({'usr':maindoc.db_username})
	result.append({'pwd':maindoc.db_password})
	#result.append({'processDate':maindoc.process_date})


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
def set_last_processed_id(datasink, table, value):
	maindoc = frappe.get_doc('Datasink',datasink)

	for item in maindoc.tables:
		if item.table_name == table:
			item.last_processed_id=value
			maindoc.save()
			return 'SUCCESS'
		
	frappe.throw(f'Table {table} does not exist in Data Source {datasink}')


