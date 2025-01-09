# 1. Import Boto3
# 2. Get the volume arn from cloud watch event
# 3. separate the volume id from volume arn using split
# 4. use volume id to modify gp2 size volume to gp3 size volume

import boto3

def get_vlolume_id_from_arn(volume_arn):
    arn_parts = volume_arn.split(':')
    volume_id = arn_parts[-1].split('/')[-1]
    return volume_id

def lambda_handler(event, context):
    volume_arn = event['resources'][0]
    volume_id = get_vlolume_id_from_arn(volume_arn)

    ec2_client = boto3.client('ec2')
    response = ec2_client.modify_volume(
        VolumeId = volume_id,
        VolumeType = 'gp3')
