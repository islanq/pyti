class FormatterTemplate:
    def __init__(self, precision=3):
        # Precision setting for floating point
        self.precision = precision
        self.align_by = None
        self.offset_by = 1
        self.center_by = None
        
        # Default templates
        self.matrix_template = "{value}"
        self.operation_swap_template = "R{row1} ↔ R{row2}"
        self.operation_mul_template = "R{row} ← R{row} ÷ {value}"
        self.operation_div_template = "R{row} ← R{row} · {value}"
        self.operation_sub_template = "R{dest_row} ← R{dest_row} - ({factor} · R{src_row})"
        self.operation_add_template = "R{dest_row} ← R{dest_row} + ({factor} · R{src_row})"
    
    def format_matrix(self, matrix):
        formatted_matrix = self._format_matrix_fixed(matrix)
        formatted_matrix = self._align(formatted_matrix)
        formatted_matrix = self._offset(formatted_matrix)
        formatted_matrix = self._center(formatted_matrix)
        return formatted_matrix
    
    def format_row(self, row):
        return self._format_row(row)
    
    def format_operation(self, op_type, i, j=None, value=None):
        if value:
            value = decimal_to_frac_str(value)
        if op_type == 'swap':
            return self.operation_swap_template.format(row1=i+1, row2=j+1)
        elif op_type == 'mul':
            return self.operation_mul_template.format(row=i+1, value=value)
        elif op_type == 'div':
            return self.operation_div_template.format(row=i+1, value=value)
        elif op_type == 'sub':
            return self.operation_sub_template.format(dest_row=i+1, src_row=j+1, factor=value)
        elif op_type == 'add':
            return self.operation_sub_template.format(dest_row=i+1, src_row=j+1, factor=value)
        return ""
    
    #region Private methods
    
    def _format_matrix_fixed(self, matrix):
        formatted = [self._format_row(row) for row in matrix]
        formatted_str = '\n'.join(formatted)
        formatted_str = self._replace_negative_zeros(formatted_str)
        return formatted_str

    def _format_value(self, value):
        if int(value) == value:
            return self._replace_negative_zeros(str(int(value)))
        str_format = "{:." + str(self.precision) + "f}"
        str_format = self._replace_negative_zeros(str_format)
        return str_format.format(value)

    def _format_row(self, row):
        formatted_values = [self._format_value(val) for val in row]
        return ', '.join(formatted_values)

    def _align(self, matrix_str):
        if not self.align_by:
            return matrix_str
        
        lines = matrix_str.split('\n')
        max_index = max(line.find(self.align_by) for line in lines if self.align_by in line)
        aligned_lines = []
        
        for line in lines:
            index = line.find(self.align_by)
            if index != -1:
                spaces = ' ' * (max_index - index)
                line = line.replace(self.align_by, spaces + self.align_by)
            aligned_lines.append(line)
        
        return '\n'.join(aligned_lines)
    
    def _offset(self, matrix_str):
        if self.offset_by <= 0:
            return matrix_str
        
        lines = matrix_str.split('\n')
        spaces = ' ' * self.offset_by
        offset_lines = [spaces + line for line in lines]
        return '\n'.join(offset_lines)
    
    def _center(self, matrix_str):
        if not self.center_by:
            return matrix_str
        
        lines = matrix_str.split('\n')
        max_length = max(len(line) for line in lines)
        centered_lines = []
        
        for line in lines:
            total_padding = max_length - len(line)
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            centered_lines.append(' ' * left_padding + line + ' ' * right_padding)
        
        return '\n'.join(centered_lines)
    
    def _replace_negative_zeros(self, matrix_str):
        negative_zero_pattern = '-0.' + '0' * self.precision
        zero_pattern = ' 0.' + '0' * self.precision
        matrix_str = matrix_str.replace(negative_zero_pattern, zero_pattern)
        matrix_str = matrix_str.replace('-0.0', ' 0.0')
        return matrix_str
    #endregion Private methods


def decimal_to_frac_str(value):
    if value == 0:
        return "0"
    # Step 1: Coarse Search
    coarse_tolerance = 1e-4
    tolerance = 1e-6
    close_values = []

    for denom in range(1, 100):  # Coarser search range
        numerator = round(value * denom)
        calculated_value = numerator / denom
        if abs(calculated_value - value) < coarse_tolerance:
            close_values.append((numerator, denom))

    # Step 2: Refinement
    refined_results = []
    refinement_range = 10  # Range around the close values to refine the search

    for close_num, close_denom in close_values:
        for denom in range(close_denom - refinement_range, close_denom + refinement_range + 1):
            if denom != 0:
                numerator = round(value * denom)
                calculated_value = numerator / denom
                if abs(calculated_value - value) < tolerance:
                    refined_results.append((numerator, denom))
                    
    # unique
    unique_results_set = set(refined_results)
    # Convert the set back to a list
    unique_results_list = list(unique_results_set)
    unique_results_list = [(num, denom) for num, denom in unique_results_list if num > 0]
    # Sort the list by the numerator
    sorted_results = sorted(unique_results_list, key=lambda x: x[0])
    if (sorted_results[0] != sorted_results[1]) and (sorted_results[0]):
        return str(value)
    fraction_str ="{}/{}".format(sorted_results[0][0], abs(sorted_results[0][1]))
    return "-" + fraction_str if value < 0 else fraction_str