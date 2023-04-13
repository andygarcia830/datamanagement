# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
from frappe.model.document import Document

class FolderManager(Document):
	pass



@frappe.whitelist()
def fetch_folder_names(storage_type,resource):
	print('FETCH FOLDER NAMES')
	folders=frappe.new_doc('Folder Objects')
	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		folders = []
		folderObjects = s3.list_objects(Bucket=resource,Delimiter='/')
		try:
			for object in folderObjects['CommonPrefixes']:
				folders.append(object['Prefix'])
		except:
			pass	
		print(f'FOLDERS={folders}')
		return folders


@frappe.whitelist()
def create_folder(storage_type,resource,object):
	
	if object[0] =='/':
		object=object[1:]

	if object[-1] != '/':
		object=object+'/'

	
	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3.put_object(Bucket=resource,Key=object)
	
