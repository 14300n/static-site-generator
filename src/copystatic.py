import os
import shutil

def copy_files_directory(source, destination):
    for item in os.listdir(source):
        full_path = os.path.join(source, item)
        if os.path.isfile(full_path):
            dest_path = os.path.join(destination, item)
            shutil.copy(full_path, dest_path)
            print(f"Copying {full_path} to {dest_path}.")
        else:
            dest_path = os.path.join(destination, item)
            os.mkdir(dest_path)
            print(f"Making {dest_path} and copying {full_path} to {dest_path}.")
            copy_files_directory(full_path, dest_path)