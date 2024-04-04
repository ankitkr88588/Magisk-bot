import os

directory_path = '/home/u201853/timer/tempo'

# Check if the directory exists
if os.path.exists(directory_path):
    # List all files in the directory
    files = os.listdir(directory_path)

    # Loop through the files and delete them one by one
    for file in files:
        file_path = os.path.join(directory_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
else:
    print(f"The directory {directory_path} does not exist.")
