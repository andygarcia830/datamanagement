# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,os
from frappe.model.document import Document

class OpenAISettings(Document):
	pass


@frappe.whitelist()
def set_key(key):
	os.environ["OPENAI_API_KEY"] = key
