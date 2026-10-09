import os
import shutil
import sys
from copystatic import copy_files_directory
from gencontent import generate_pages_recursive

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copy_files_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    





main()