# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe,boto3,os
import datamanagement.data_management.doctype.aws_configuration.aws_configuration
from frappe.model.document import Document

class AWSS3BucketManager(Document):
	pass

@frappe.whitelist()
def fetch_buckets():
    datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
    maindoc = frappe.get_doc('AWS S3 Bucket Manager')
    s3 = boto3.resource('s3')
    bucketObjects = maindoc.buckets
    print(f'GOT BUCKETS {bucketObjects}')
    SQL='UPDATE `tabS3Buckets` t SET t.exists=0;'
    
    frappe.db.sql(SQL)
    
    bucketNames=[]
    for entry in bucketObjects:
        #print(entry.name)
        thisBucket=frappe.get_doc('S3Buckets',entry.name)
        bucketNames.append(thisBucket.name)
	    #thisBucket.delete()
    
    print(bucketNames)
    
    for bucket in s3.buckets.all():
        if bucketNames.count(bucket.name) ==0:
            print(f'BUCKET {bucket.name} NOT IN DATABASE')
            bucketEntry = maindoc.append('buckets',{})
            print(bucket.name)
            bucketEntry.bucket=bucket.name
            bucketEntry.exists=1
        else:
            print(f'BUCKET {bucket.name} IN DATABASE')
            SQL=f'UPDATE `tabS3Buckets` t SET t.exists=1 WHERE t.bucket=\'{bucket.name}\';'
            frappe.db.sql(SQL)
    
    SQL='DELETE FROM `tabS3Buckets` WHERE `tabS3Buckets`.exists=0;'
    frappe.db.sql(SQL)
    maindoc.save()
	#return str(buckets)


@frappe.whitelist()
def create_bucket(bucket):
    datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
    s3 = boto3.client('s3')
    print(f'BUCKET NAME = {bucket}')
    region = os.environ['AWS_DEFAULT_REGION']
    response = s3.create_bucket(
    ACL='private',
    Bucket=bucket,
     CreateBucketConfiguration={
        'LocationConstraint': region
    },
	)
    fetch_buckets()
    frappe.msgprint(str(response))
    

@frappe.whitelist()
def delete_bucket(bucket):
    datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials()
    s3 = boto3.client('s3')
    print(f'BUCKET NAME = {bucket}')
    region = os.environ['AWS_DEFAULT_REGION']
    response = s3.delete_bucket(
    Bucket=bucket,
   )
    fetch_buckets()
    frappe.msgprint(str(response))