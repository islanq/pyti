import sys
import os

if not sys.platform == 'TI-Nspire':
    if not 'lib' in sys.path:
        # Get the directory of the __init__.py file
        project_root = os.path.dirname(os.path.abspath(__file__))
        # Define the subfolder you want to add to the path
        subfolder = 'lib'
        # Construct the full path to the subfolder and normalize it
        subfolder_path = os.path.normpath(os.path.join(project_root, subfolder))
        # Append the subfolder path to sys.path
        sys.path.append(subfolder_path)
    if not '..' in sys.path:
        sys.path.append('..')
    if not '.\\lib' in sys.path:
        sys.path.append('.\\lib')