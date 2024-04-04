import urwid
import urllib.request

# Function to fetch a webpage and return its content
def fetch_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as e:
        return str(e)

# Function to display a webpage
def display_webpage(url):
    content = fetch_url(url)
    return urwid.Text(content)

# Main function
def main():
    url = "https://www.needrom.com/download/infinix-note-30-5g-x6711/"  # Replace with the URL you want to browse
    webpage = display_webpage(url)
    

