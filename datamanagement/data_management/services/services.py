import frappe,boto3
import datamanagement.data_management.doctype.aws_configuration.aws_configuration

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
def fetch_empty_folder_names(storage_type,resource):
	print(f'FETCH EMPTY FOLDER NAMES {storage_type} {resource}')
	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		# Let's use Amazon S3
		s3 = boto3.client('s3')
		s3r = boto3.resource('s3')
		folders = []
		folderObjects = s3.list_objects(Bucket=resource,Delimiter='/')
		for object in folderObjects['CommonPrefixes']:
			folder=object['Prefix']
			bucket=s3r.Bucket(resource)
			objs = bucket.objects.filter(Prefix=folder)
			objlist=list(objs)
			thisobj=objlist[0]
			thiskey=thisobj['key']
			print(f'FOUND FOLDER {folder} {thiskey}')
			if len(list(objlist)) ==1:
				folders.append(folder)
		#except:
	    #pass	
		print(f'FOLDERS={folders}')
		return folders


@frappe.whitelist()
def delete_empty_folder(storage_type,resource,folder):
	# if folder[-1]=='/':
	# 	folder=folder[:-1]
	print(f'DELETE EMPTY FOLDER NAMES {storage_type} {resource} {folder}')

	if storage_type=='AWS S3':
		datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
		s3 = boto3.client('s3')
		print(f'OBJECT NAME = {folder}')
		response = s3.delete_object(
		Bucket=resource,
		Key=folder
		)
		frappe.msgprint(f"Deleted Folder {folder} {response}")
		return response
	


@frappe.whitelist()
def get_airflow_url():
	maindoc=frappe.get_doc('DeveloperPortalSettings')
	return maindoc.airflow_url