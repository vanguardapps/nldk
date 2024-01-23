def get_file_lines(filepath, start_line, end_line):
    """
    Gets a range of lines from a text file located at filepath, returns as array of strings (lines)

    """
    line_count = 0
    lines = []
    with open(filepath, "r") as file:
        for line in file:
            if line_count >= start_line and line_count <= end_line:
                lines.append(line)
            elif line_count > end_line:
                break
            line_count += 1
    return lines


def print_file_lines(in_path, start_line, end_line, out_path):
    """
    Sends a select range of lines in a file to `stdout` as-is.

    @param in_path (str):           The path to the file.
    @param start_line (int):        The beginning of the line range (included in output)
    @param end_line (int):          The end of the line range (not included in output)
    @param out_path (str):          The desired output filepath.

    """
    start_line = int(start_line)
    end_line = int(end_line)
    with open(out_path, "w") as output_file:
        output_file.writelines(get_file_lines(in_path, start_line, end_line))
    print(
        f"Output '{in_path}' lines {start_line} through {end_line} to new file '{out_path}'"
    )
