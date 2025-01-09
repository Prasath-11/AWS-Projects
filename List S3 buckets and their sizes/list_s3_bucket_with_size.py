import boto3
from botocore.exceptions import NoCredentialsError

def get_s3_buckets_and_sizes():
    # Create a session using the default AWS profile
    s3 = boto3.client('s3')

    try:
        # List all S3 buckets
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])

        if not buckets:
            print("No S3 buckets found.")
            return

        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f"\nBucket: {bucket_name}")
            total_size = 0
            object_count = 0

            # Get the size of all objects in the bucket
            try:
                # List objects in the bucket
                paginator = s3.get_paginator('list_objects_v2')
                for page in paginator.paginate(Bucket=bucket_name):
                    for obj in page.get('Contents', []):
                        total_size += obj['Size']
                        object_count += 1

                # Convert bytes to GB for easier reading
                total_size_gb = total_size / (1024 ** 3)

                print(f"Total Size: {total_size_gb:.2f} GB")
                print(f"Number of Objects: {object_count}")
            except Exception as e:
                print(f"Error retrieving objects for bucket {bucket_name}: {str(e)}")

    except NoCredentialsError:
        print("Error: No valid AWS credentials found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    get_s3_buckets_and_sizes()
