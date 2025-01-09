import os
import time

# Directory to monitor
WATCHED_DIR = '/home/ubuntu/parent_dir/src_dir/'

# Size threshold in bytes (100 MB)
SIZE_THRESHOLD = 100 * 1024 * 1024  # 100 MB in bytes

def monitor_directory(directory):
    """Monitor the specified directory and delete files larger than SIZE_THRESHOLD."""
    while True:
        # List all files in the directory
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)

                # Check if it is a file and if it's larger than the threshold
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)

                    # If file is larger than 100 MB, delete it
                    if file_size > SIZE_THRESHOLD:
                        print(f"File {file_path} is larger than 100 MB ({file_size / (1024 * 1024):.2f} MB). Deleting...")
                        os.remove(file_path)
                        print(f"File {file_path} deleted.")
        
        except Exception as e:
            print(f"Error accessing directory {directory}: {e}")
        
        # Wait for a minute before checking again
        time.sleep(60)

if __name__ == "__main__":
    print(f"Monitoring directory: {WATCHED_DIR}")
    monitor_directory(WATCHED_DIR)
