# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkerInstanceDispatcher(Document):
	pass


@frappe.whitelist()
def fetch_worker(dag_id):
	maindoc = frappe.get_doc('Worker Instance Dispatcher',dag_id)
	child = frappe.get_doc('Worker Instance',maindoc.worker_instance)
	result={}
	result['name']=child.name1
	result['host']=child.host
	result['login']=child.login
	result['other_parameters']=child.other_parameters
	
	return result
