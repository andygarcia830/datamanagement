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


