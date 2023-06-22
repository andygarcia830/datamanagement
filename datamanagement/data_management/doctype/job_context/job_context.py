# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
import datamanagement.data_management.doctype.data_folder.data_folder
from frappe.model.document import Document

class JobContext(Document):
	pass


@frappe.whitelist()

def fetch_client_data():
	maindoc = frappe.get_doc('Client Configuration')
	result = {}
	result['storage_type']= maindoc.storage_type
	result['client_namespace']= maindoc.client_namespace
	return result


@frappe.whitelist()
def fetch_job_context(id):
	globaldoc = frappe.get_doc('Client Configuration')
	maindoc = frappe.get_doc('Job Context',id)
	maindoc.storage_type = globaldoc.storage_type
	maindoc.client_namespace = globaldoc.client_namespace
	print(f'JOB CONTEXT={maindoc}')
	for item in maindoc.dependencies:
		source=frappe.get_doc('Job Context',item.source_job_context)
		source.storage_type=maindoc.storage_type
		item.source_job_context = source
	

	return maindoc
