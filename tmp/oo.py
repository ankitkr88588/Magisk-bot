import urllib.request

url = input("Link: ")

try:
    response = urllib.request.urlopen(url)
    if "Content-Length" in response.headers:
        content_length = int(response.headers["Content-Length"])
        print(f"File size: {content_length} bytes")
        if content_length > (4 * 1024 * 1024 * 1024):  # Check if file size exceeds 4 GB
            print("File size exceeds 4 GB. Aborting download.")
            # Proceed with downloading the file
    else:
            # You can add your download code here
        print("Content length not found in headers. Cannot determine file size.")
except urllib.error.URLError as e:
    print(f"An error occurred: {e}")

