import subprocess

file_path = "filePath"  # Replace with the actual file path
key = "key"  # Replace with the actual key

if not file_path:
    print("File path is missing. Please provide a valid file path.")
else:
    command = f'curl -s https://devuploads.com/upload.sh | bash -s -- -f {file_path} -k {key}'
    completed_process = subprocess.run(command, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, text=True)
    print(completed_process.stdout)

