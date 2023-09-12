def display_matrices(matrices):
    """Display a list of matrices side by side in a formatted way with .format method."""

    # Get the maximum width of each column in each matrix
    col_widths = [
        [max(len(str(row[i])) for row in matrix)
         for i in range(len(matrix[0]))]
        for matrix in matrices
    ]

    # Create a formatted string for each row
    rows = []

    # Get the number of rows in each matrix
    num_rows = [len(matrix) for matrix in matrices]

    # Get the maximum number of rows across all matrices
    max_rows = max(num_rows)

    for idx in range(max_rows):
        row_strs = []
        for m, matrix in enumerate(matrices):
            if idx < num_rows[m]:
                row = matrix[idx]
                row_str = (
                    "⎡" + "  ".join("{:>{}}".format(str(row[i]), col_widths[m][i]) for i in range(len(row))) + "⎤" if idx == 0
                    else "⎢" + "  ".join("{:>{}}".format(str(row[i]), col_widths[m][i]) for i in range(len(row))) + "⎥" if idx != num_rows[m] - 1
                    else "⎣" + "  ".join("{:>{}}".format(str(row[i]), col_widths[m][i]) for i in range(len(row))) + "⎦"
                )
            else:
                row_str = " " * \
                    (sum(col_widths[m]) + len(col_widths[m]) * 2 - 1)

            row_strs.append(row_str)

        # Join the formatted strings for the current row from all matrices
        rows.append(" ".join(row_strs))

    # Join the rows with newline characters to get the final string
    matrix_str = "\n".join(rows)

    return matrix_str


print(display_matrices(
    [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2], [3, 4], [5, 6]]]))
