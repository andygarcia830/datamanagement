import frappe,boto3

@frappe.whitelist()
def test_aws():
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    # Print out bucket names
    buckets = []
    for bucket in s3.buckets.all():
        print(bucket.name)
        buckets.append(bucket.name)
    return str(buckets)