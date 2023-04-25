# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3,os
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.utils import now

class DataFolder(Document):
	pass

@frappe.whitelist()
def fetch_resource_names(storage_type):

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
def fetch_folder_names(storage_type,resource):
	print('FETCH FOLDER NAMES')
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
def fetch_objects(storage_type,name):
	maindoc = frappe.get_doc('Data Folder',name)
	print(f'GOT FOLDER {maindoc}')
	subfolder=maindoc.folder
	if storage_type=='AWS S3':
		bucket = maindoc.resource
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
		FolderObjects=s3.list_objects(Bucket=bucket,Prefix=subfolder)
		print(f'FOLDER OBJECTS={FolderObjects}')
		for object in FolderObjects['Contents']:
			try:
				#print(f'THIS OBJECT={object}')
				thisObjectName=object['Key']
				print(f'FOUND {thisObjectName}')
				print(f'LEN= {len(subfolder)}')
				
				thisObjectName=thisObjectName[len(subfolder)::]
				print(f'SUBSTRING \'{thisObjectName}\'')
				# only save what is in the specified folder
			
				if len(thisObjectName) > 0 and objectNames.count(thisObjectName) ==0:
					print(f'Object {thisObjectName} NOT IN DATABASE')
					objectEntry = maindoc.append('objects',{})
					print(thisObjectName)
					objectEntry.object=thisObjectName
					objectEntry.exists=1
				else:
					if len(thisObjectName) > 0:
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
def upload_object(name,file,subdirectory):
	maindoc = frappe.get_doc('Data Folder',name)
	storage_type=maindoc.storage_type
	folder= maindoc.folder
	print(f'file={file}')
	if subdirectory[0] =='/':
		subdirectory=subdirectory[1:]

	subdirectory=folder+subdirectory

	key = file[file.rindex('/')+1:]
	key = subdirectory + key
	print(f'key={key}')
	file = './'+cstr(frappe.local.site)+file
	if storage_type=='AWS S3':
		bucket=maindoc.resource
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3.upload_file(file,bucket , key)
	fetch_objects(storage_type,name)
	maindoc.reload()
	# remove temporary file
	if os.path.isfile(file):
		os.remove(file)

@frappe.whitelist()
def create_folder(name,object):
	maindoc = frappe.get_doc('Data Folder',name)
	storage_type=maindoc.storage_type
	resource=maindoc.resource
	folder=maindoc.folder
	
	if object[0] =='/':
		object=object[1:]

	if object[-1] != '/':
		object=object+'/'

	object=folder+object


	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3.put_object(Bucket=resource,Key=object)
	fetch_objects(storage_type,name)
	maindoc.reload()



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
def fetch_access(metadata):
	maindoc = frappe.get_doc('MetaData',metadata)
	result = {}
	result['data_owner'] = maindoc.owner
	result['data_stewards'] = maindoc.steward
	return result 



@frappe.whitelist()
def delete_object(name,object):
	maindoc = frappe.get_doc('Data Folder',name)
	storage_type=maindoc.storage_type
	resource=maindoc.resource
	folder=maindoc.folder
	object=folder+object
	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		s3 = boto3.client('s3')
		print(f'OBJECT NAME = {object}')
		region = os.environ['AWS_DEFAULT_REGION']
		response = s3.delete_object(
		Bucket=resource,
		Key=object
		)
		fetch_objects(storage_type,name)
		maindoc.reload()
		frappe.msgprint(str(response))

@frappe.whitelist()
def fetch_metadata(name):
	metadata=frappe.get_all('MetaData', filters={'data_folder': name}, fields=['name'])
	print(f'GOT METADATA {metadata}')
	if len(metadata) > 0:
		md= metadata[0]
		return md['name']
	

@frappe.whitelist()
def submit_log(folder,message,entry_count):
	maindoc = frappe.get_doc('Data Folder',folder)
	logtable=maindoc.logs
	print(f'GOT FOLDER {folder} {entry_count} {message}')
	logentry=maindoc.append('logs',{})
	logentry.date=now(),
	logentry.message=message,
	logentry.entry_count=entry_count
	logtable=maindoc.logs
	print(f'GOT LOGS {logtable}')
	
	maindoc.save()
	print(f'GOT LOGS {logtable}')
	return 'SUCCESS'
