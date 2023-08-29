import os
def adjust_python_indentation(input_filename, desired_indent=4, outdir=None):
    
    output_directory = outdir if outdir else './ti_converted'
    output_filename = os.path.join(output_directory, "ti_" + os.path.basename(input_filename)).replace('\\', '/')
    
    if not os.path.exists(input_filename):
        raise FileNotFoundError("Input file does not exist: " + input_filename)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

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

adjust_python_indentation('shunting_yard.py', 2)