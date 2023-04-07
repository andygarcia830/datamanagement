# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document

class AWSConfiguration(Document):
	pass

@frappe.whitelist()
def import_aws_credentials():
	aws = frappe.get_doc('AWS Configuration')
	print(f'AWS CONFIGURATION={aws}')
	os.environ['AWS_ACCESS_KEY_ID']=aws.aws_access_key_id
	os.environ['AWS_SECRET_ACCESS_KEY']=aws.aws_secret_access_key
	os.environ['AWS_DEFAULT_REGION']=aws.aws_default_region