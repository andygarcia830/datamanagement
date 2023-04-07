# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3,os
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
from frappe.model.document import Document
from frappe.utils import cstr

class DataFolder(Document):
	pass

@frappe.whitelist()
def fetch_folder_names(storage_type):

	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.resource('s3')
		buckets = []
		
		for bucket in s3.buckets.all():
			buckets.append(bucket.name)
		print(buckets)	
		return buckets


@frappe.whitelist()
def fetch_objects(storage_type,name):
	maindoc = frappe.get_doc('Data Folder',name)
	print(f'GOT FOLDER {maindoc}')
	if storage_type=='AWS S3':
		bucket = maindoc.folder
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Clear current list
		objects = maindoc.objects
		SQL='UPDATE `tabFolderObjects` t SET t.exists=0;'
		frappe.db.sql(SQL)
		objectNames=[]
		
		for entry in objects:
			thisObject=frappe.get_doc('FolderObjects',entry.name)
			objectNames.append(thisObject.object)
	    
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		FolderObjects=s3.list_objects(Bucket=bucket)
		print(f'FOLDER OBJECTS={FolderObjects}')
		try:
			for object in FolderObjects['Contents']:
				#print(f'THIS OBJECT={object}')
				thisObjectName=object['Key']

				if objectNames.count(thisObjectName) ==0:
					print(f'Object {thisObjectName} NOT IN DATABASE')
					objectEntry = maindoc.append('objects',{})
					print(thisObjectName)
					objectEntry.object=thisObjectName
					objectEntry.exists=1
				else:
					print(f'Object {thisObjectName} IN DATABASE')
					SQL=f'UPDATE `tabFolderObjects` t SET t.exists=1 WHERE t.object=\'{thisObjectName}\';'
					frappe.db.sql(SQL)
				print(object['Key'])
		except:
			pass

		
		SQL='DELETE FROM `tabFolderObjects` WHERE `tabFolderObjects`.exists=0;'
		frappe.db.sql(SQL)
		maindoc.save()	
		

@frappe.whitelist()
def upload_object(storage_type,name,file,subdirectory):
	maindoc = frappe.get_doc('Data Folder',name)
	print(f'file={file}')
	if subdirectory[0] =='/':
		subdirectory=subdirectory[1:]

	key = file[file.rindex('/')+1:]
	key = subdirectory + key
	print(f'key={key}')
	file = './'+cstr(frappe.local.site)+file
	if storage_type=='AWS S3':
		bucket=maindoc.folder
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3.upload_file(file,bucket , key)
	fetch_objects(storage_type,name)

@frappe.whitelist()
def create_folder(storage_type,name,folder,object):
	maindoc = frappe.get_doc('Data Folder',name)
	
	if object[0] =='/':
		object=object[1:]

	if object[-1] != '/':
		object=object+'/'


	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3.put_object(Bucket=folder,Key=object)
	fetch_objects(storage_type,name)


@frappe.whitelist()
def get_subfolder_names(name):
	maindoc = frappe.get_doc('Data Folder',name)
	objects = maindoc.objects
	folderNames=['/']
	for entry in objects:
		thisObject=frappe.get_doc('FolderObjects',entry.name)
		objectName=thisObject.object

		try:
			slashIndex=objectName.rindex('/')+1
			objectName = objectName[0:slashIndex]
			folderList=objectName.split('/')
			subFolder='/'
			for part in folderList:
				if len(part) > 0:
					subFolder=subFolder+part+'/'
					if len(subFolder) > 0 and folderNames.count(subFolder) == 0:
						folderNames.append(subFolder)	
			objectName=''

		except:
			objectName='/'
			pass

		if len(objectName) > 0 and folderNames.count(objectName) == 0:
			folderNames.append(objectName)
	folderNames.sort()
	return folderNames 



@frappe.whitelist()
def delete_object(storage_type,name,folder,object):
	
	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		s3 = boto3.client('s3')
		print(f'OBJECT NAME = {object}')
		region = os.environ['AWS_DEFAULT_REGION']
		response = s3.delete_object(
		Bucket=folder,
		Key=object
		)
		fetch_objects(storage_type,name)
		frappe.msgprint(str(response))