import time
import os
from pathlib import Path
import shutil  # Import the shutil module for file copying

# Specify the directory path
def get_files(path, extension, recursive=True):
    path = Path(path) if isinstance(path, str) else path
    return list(Path(path).rglob(extension) if recursive else path.glob(extension))

# Use glob to find all .py files in the directory and its subdirectories

def compare_files(file_path1, file_path2):
    """
    Compare the contents of two files to check if they are identical.

    Args:
    file_path1 (str): The path to the first file.
    file_path2 (str): The path to the second file.

    Returns:
    bool: True if the contents are identical, False otherwise.
    """
    with open(file_path1, 'r', encoding='utf-8') as file1, open(file_path2, 'r', encoding='utf-8') as file2:
        return file1.read() == file2.read() 


target_files = get_files('C:\\Users\\islan\\AppData\\Roaming\\Texas Instruments\\TI-Nspire CX CAS Student Software\\python', '*.py')
source_files = get_files('.\\lib', '*py', False) + get_files('.', '*.py',False) + get_files('.\\solvers', '*.py', False)


if target_files is None or len(target_files) == 0:
    print("No files found.")



# Create a dictionary to store file names and paths from the source_files list
source_file_dict = {file.name: file for file in source_files}

# Iterate through target_files and compare with source_files
for target_file in target_files:
    target_file_name = target_file.name
    if target_file_name in source_file_dict:
        source_file = source_file_dict[target_file_name]
        if not compare_files(target_file, source_file):
            shutil.copyfile(source_file, target_file)
            print(f"Updated {target_file_name}")