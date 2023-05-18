# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkerInstance(Document):
	pass


@frappe.whitelist()
def submit_log(name,job_name,cpu_usage,memory_usage,message,start,end):
	parent = frappe.get_doc('Worker Instance',name)
	row = parent.append('logs')
	row.job_name=job_name
	row.cpu_usage=cpu_usage
	row.memory_usage=memory_usage
	row.message=message
	row.start=frappe.utils.get_datetime(start)
	row.end=frappe.utils.get_datetime(end)

	print(f'START={row.start}')
	# row.start=frappe.utils.now()
	# row.end=frappe.utils.now()
	parent.save()

	return 'SUCCESS'