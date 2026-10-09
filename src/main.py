import os
import shutil
from copystatic import copy_files_directory
from gencontent import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_files_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")




main()