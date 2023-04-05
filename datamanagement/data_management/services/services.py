import frappe,boto3

@frappe.whitelist()
def test_aws(name):
    maindoc = frappe.get_doc('AWS Test',name)
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    # Print out bucket names
    buckets = []
    for bucket in s3.buckets.all():
        bucketEntry = maindoc.append('test',{})
    
        print(bucket.name)
        buckets.append(bucket.name)
        bucketEntry.bucket=bucket.name

       
    maindoc.save()
    return str(buckets)