# 1. boto3 Module import
# 2. def lambda 
# 3. describe snapshots
# 4. describe instances
# 5. if volume is not associated with active instances --> delete snapshot
# 6. if snapshot is not associated wtih any volume --> delete snapshot

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    active_instance_ids = set()

    snapshot_response = ec2.describe_snapshots(ownerIds = ['self'])

    instance_response = ec2.describe_instances(Filters = [{'Name':'instance-state-name', 'value':['Running']}])

    for reservation in instance_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance)

    for snapshot in snapshot_response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']

        if not volume_id:
            ec2.delete_snapshots(SnapshotId = snapshot_id)
            print(f"Deleted {snapshot_id} as it not attached to any active volumes")

        else:
            try:
                volume_response = ec2.describe_volumes(VolumeIds =[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshots(SnapshotId = snapshot_id)
                    print(f"Deleted {snapshot_id} as the assciated volume is not attched to any active instances")
            except ec2.exceptions.clientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    ec2.delete_snapshots(SnapshotId = snapshot_id)
                    print(f"Deleted {snapshot_id} as the assciated volume is not found")                   