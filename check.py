import requests
import os

url = input("link:")
download_directory = "/home/u201853/tmp" # Directory where you want to save the downloaded file

try:
    response = requests.head(url)  # Send a HEAD request to fetch only headers
    if "content-type" in response.headers:
        content_type = response.headers["content-type"]
        if "text/html" not in content_type:  # Check if it's not an HTML page
            if "content-length" in response.headers:
                content_length = int(response.headers["content-length"])
                print(f"The URL points to a file with content type: {content_type}")
                print(f"File size: {content_length} bytes")

                # Create the download directory if it doesn't exist
                if not os.path.exists(download_directory):
                    os.makedirs(download_directory)

                # Download the file
                filename = os.path.join(download_directory, url.split("/")[-1])
                response = requests.get(url)
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"File downloaded to {filename}")
            else:
                print("Content length not found in headers. Cannot determine file size.")
        else:
            print("The URL may not point to a file.")
    else:
        print("Content type not found in headers. Cannot determine if it's a file or not.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

