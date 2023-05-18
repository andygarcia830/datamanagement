# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkerInstanceDispatcher(Document):
	pass


@frappe.whitelist()
def fetch_worker(dag_id):
	maindoc = frappe.get_doc('Worker Instance',dag_id)
	print(f'JOB CONTEXT={maindoc}')
	return maindoc
