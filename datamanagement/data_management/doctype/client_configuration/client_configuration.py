# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3,os
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
from frappe.model.document import Document

class ClientConfiguration(Document):
	pass


@frappe.whitelist()
def create_bucket(storage_type,name):
	print('CREATE')
	
	if (storage_type=='AWS S3'):
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		s3 = boto3.client('s3')
		print(f'BUCKET NAME = {name}')
		region = os.environ['AWS_DEFAULT_REGION']
		response = s3.create_bucket(
		ACL='private',
		Bucket=name,
			CreateBucketConfiguration={
			'LocationConstraint': region
		},
		)
		print(f'RESPONSE = {response}')

