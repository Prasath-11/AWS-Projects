import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    active_instance_ids = set()

    snapshot_response = ec2.describe_snapshots(ownerIds =['self'])
    instance_response = ec2.describe_instance(Filters = [{'Name' : 'instance-state-name','Values': ['Running']}])

    for reservation in instance_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance)

    for snapshot in snapshot_response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']

    if not volume_id:
        ec2.delete_snapshots(SnapshotId = snapshot_id)
        print(f"Deleted {snapshot_id} as it not attaced to any active volumes")

    else:
        try:
            volume_response = ec2.describe_volumes(VolumeId =volume_id)
            if not volume_response['Volumes'][0]['Attachments']:
                ec2.delete_snapshots(SnapshotId = snapshot_id)
                print(f"Deleted {snapshot_id} as the associated volume is not attached to any active instances")
        except ec2.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                ec2.delete_snapshots(SnapshotId = snapshot_id)
                print(f"Deleted {snapshot_id} as the associated volume is not found")

