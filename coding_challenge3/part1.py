import os

from pathlib import Path

parent_directory = r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\new_dir"
#os.mkdir(parent_directory)

dirs_main = ["draft code", "includes", "layouts", "site"]

for file in dirs_main:
    os.mkdir(os.path.join(parent_directory, file))

dirs_sub = ["pending", "complete", "default", "post", "posted"]

counter = 0
first_directory = r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\new_dir\draft code"
second_directory = r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\new_dir\layouts"
third_directory = r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\new_dir\layouts\post"

for file in dirs_sub:
    counter += 1
    if counter <= 2:
        os.mkdir(os.path.join(first_directory, file))
    elif counter > 2 and counter <=4:
        os.mkdir(os.path.join(second_directory, file))
    else:
        os.mkdir(os.path.join(third_directory, file))

import shutil
shutil.rmtree(r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\new_dir")

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

rmdir(Path(r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\new_dir"))
