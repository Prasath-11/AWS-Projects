import boto3
from datetime import datetime
import pytz

# Set the timezone to your desired time zone (e.g., 'US/Eastern' or 'UTC')
timezone = pytz.timezone('US/Eastern')

# Initialize the EC2 client
ec2 = boto3.client('ec2')

# List of EC2 instance IDs you want to manage
INSTANCE_IDS = ['i-039d03ba45a5797ce']  # Example EC2 instance IDs

def get_current_time():
    """Returns the current time in the specified timezone."""
    return datetime.now(timezone)

def start_instances():
    """Starts the EC2 instances."""
    print("Starting EC2 instances...")
    ec2.start_instances(InstanceIds=INSTANCE_IDS)
    print("EC2 instances started.")

def stop_instances():
    """Stops the EC2 instances."""
    print("Stopping EC2 instances...")
    ec2.stop_instances(InstanceIds=INSTANCE_IDS)
    print("EC2 instances stopped.")

def main():
    """Main function to start/stop instances based on the time."""
    current_time = get_current_time()
    current_hour = current_time.hour

    print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # If it's 8 AM or later but before 8 PM, start the instances
    if current_hour >= 8 and current_hour < 20:
        print("Checking to start instances...")
        start_instances()
    # If it's 8 PM or later, stop the instances
    elif current_hour >= 20 or current_hour < 8:
        print("Checking to stop instances...")
        stop_instances()

if __name__ == "__main__":
    main()
