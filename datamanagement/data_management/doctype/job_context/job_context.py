# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
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