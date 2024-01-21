from write_csv_line import write_csv_line


def tsv2csv(in_path, out_path):
    """
    Converts TSV files to CSV files.

    @param in_path (str):   The filepath to the input TSV file.
    @param out_path (str):  The filepath to the desired output CSV file.

    LIMITATION: will not handle CRLF characters in the TSV, as it reads file line by line.
    This is not important for most datasets, and does not negatively affect results using
    the data included in this repo.

    """
    with open(out_path, "w") as output_file:
        with open(in_path) as input_file:
            for line in input_file:
                write_csv_line(output_file, line.rstrip().split("\t"))
    print(f"Converted '{in_path}' from TSV to CSV. Result stored in '{out_path}'")
