import os
import re

def is_fstring(string):
    pattern = re.compile(r'^f[\'\"].*?[\'\"]$')
    return bool(pattern.search(string))

def write_output(output_file_path, lines):
    
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(lines)

def adjust_python_indentation(input_filename, desired_indent=4, outdir=None):
    
    output_directory = outdir if outdir else './ti_converted'
    output_prefix = "ti_" if not "ti_" in input_filename else ""
    output_filename = os.path.join(output_directory, output_prefix + os.path.basename(input_filename)).replace('\\', '/')
    
    if not os.path.exists(input_filename):
        raise FileNotFoundError("Input file does not exist: " + input_filename)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    if is_fstring('\n'.join(lines)):
        raise ValueError("Input file contains f-strings: " + input_filename)

    fixed_lines = []
    indent_stack = [0]  # Stack to keep track of indents for each scope

    for line in lines:
        line_stripped = line.lstrip()
        line_indent = len(line) - len(line_stripped)

        # Ignore empty lines
        if not line_stripped:
            fixed_lines.append(line)
            continue

        # Check for scope changes
        while indent_stack and line_indent < indent_stack[-1]:
            indent_stack.pop()
        if line_indent > indent_stack[-1]:
            indent_stack.append(line_indent)

        # Calculate new indent level based on the stack length
        new_indent_level = len(indent_stack) - 1  # -1 to discount the initial 0

        # Create new line with adjusted indent
        fixed_lines.append(" " * (new_indent_level * desired_indent) + line_stripped)

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.writelines(fixed_lines)
    
    return output_filename

def merge_python_files(file_paths, out_name, outdir=None):
    
    outdir = outdir if outdir else './merged'
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    
    with open(f'{outdir}/merged_{out_name}', 'w', encoding='utf-8') as output_file:
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as input_file:
                content = input_file.read()
                output_file.write(f"# Merged content from {file_path}\n")
                output_file.write(content)
                output_file.write("\n\n")

adjust_python_indentation('./ti_interop.py', 2)
#merge_python_files(['./matrix.py', './queue_print.py', './matrix_format.py'], 'matrix.py')