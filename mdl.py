import mediafire_dl

url = input("dena:")
output = 'file.zip'
mediafire_dl.download(url, output, quiet=False)
