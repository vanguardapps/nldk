def write_csv_line(file_object, items):
    """
    Given an open file object and list of strings, add them as a properly-formatted and
    escaped line to the CSV file object.

    @param file_object (io.TextIOWrapper): a target file object to write the line of CSV data
    @param items (List[str]): a list of strings to be added in order as a line to the CSV file
    @returns csv_line: the actual csv_line (including newline) that was written to the CSV file
    """

    # Format the line to write
    csv_line = (
        # Escape any double quotes as double double quotes
        ",".join(['"' + value.replace('"', '""') + '"' for value in items])
        + "\n"
    )

    file_object.write(csv_line)

    # Return formatted line back to caller
    return csv_line
