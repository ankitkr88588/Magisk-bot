import os
import zipfile

def unzip_files():
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        if file.endswith(('.apk', '.zip')):
            file_path = os.path.join(current_directory, file)
            folder_name = os.path.splitext(file)[0]
            folder_path = os.path.join(current_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            print(f"Extracted {file} into {folder_name}")

unzip_files()
