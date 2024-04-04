import subprocess
import requests

url = input("Link: ")
download_directory = "/home/u201853/tmp"  # Directory where you want to save the downloaded file
max_file_size_bytes = 4 * 1024 * 1024 * 1024  # 4 GB in bytes

try:
    # Send a HEAD request to fetch only headers and check file size
    response = requests.head(url)
    if "content-length" in response.headers:
        content_length = int(response.headers["content-length"])
        if content_length > max_file_size_bytes:
            print("File size exceeds 4 GB. Aborting download.")
        else:
            print(f"File size: {content_length} bytes")

            # Download the file with wget and show progress
            command = ["wget", url, "--progress=bar:force", "-P", download_directory]
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Redirect stderr to stdout
                text=True
            )
            for line in process.stdout:
                print(line.strip())
            process.wait()  # Wait for the process to finish
            if process.returncode == 0:
                print(f"File downloaded successfully to {download_directory}")
            else:
                print("Download failed. Please check the URL.")
    else:
        print("Content length not found in headers. Cannot determine file size.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

