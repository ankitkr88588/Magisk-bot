import subprocess

# Define the file you want to upload and the Transfer.sh URL
file_to_upload = "dhdhd.py"
transfer_url = "https://transfer.sh"

# Use subprocess to run the curl command
try:
    upload_result = subprocess.check_output(
        ["curl", "--upload-file", file_to_upload, transfer_url],
        universal_newlines=True
    )
    
    # Print the upload result
    print(upload_result)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

