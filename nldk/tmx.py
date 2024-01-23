from xml.sax import parse, SAXParseException
from xml.sax.handler import ContentHandler
import io, os


class TMXColumnParser(ContentHandler):
    def __init__(
        self,
        xml_file_object,
        file_size_in_bytes,
        column_names=None,
        write_row=None,
        verbose_output=None,
        status_update_frequency_bytes=None,
        content_direct_parent=None,
        content_row_divider=None,
        experimental=None,
    ):
        """

        xml_file_object                     File object (already opened) that the parser will be working off of

        file_size_in_bytes                  File size in bytes of the file to which xml_file_object refers

        write_row                           Lambda to perform write of individual row of TMX data (one translation unit
                                            of semantically equivalent segments differing by language) Default is to print the
                                            list of extracted content values to the console.

                                            Note: if a column does not have a value, an empty string will be placed in that
                                            ordinal position in the list of content values received.

                                            Note: columns will appear in the same order as they are given in the constructor
                                            parameter `column_names`

        verbose_output                   Boolean to determine whether to output verbosely to console

        status_update_frequency_bytes       Number of bytes to traverse before updating the status bar with a new percentage.
                                            Defaults to file_size_in_bytes / 1000 for updates every tenth of a percent. Set
                                            to 0 to disable status updates specifically.

        content_direct_parent               Tells the parser which element directly contains the sections of content.
                                            Defaults to "seg" for TMX files.

        content_row_divider                 Tells the parser which element represents the division between rows of content.
                                            Defaults to "tu" for TMX files (as various translations of one sentence are often
                                            contained within one enclosing <tu>...</tu> tag).

        column_names                        List of column names. Informs the parser of:
                                                - How many languages (or columns, generally) are contained within each row.
                                                - What to call those columns if that data becomes useful in future enhancements

        experimental                        Boolean value to toggle experimental functionality on and off. Default is False.

        """

        FILE_SIZE_MINIMUM_BYTES = 10

        self._experimental = experimental if experimental else False

        # Validate that xml_file_object is indeed an instance of io.TextIOWrapper class
        if not isinstance(xml_file_object, io.TextIOWrapper):
            raise ValueError(
                "Parameter 'xml_file_object' must be member of io.TextIOWrapper class (must be a file object)"
            )

        # Validate that file_size_in_bytes has been provided
        if not file_size_in_bytes:
            raise ValueError("Parameter 'file_size_in_bytes [long]' is required")

        file_size_in_bytes = int(file_size_in_bytes)

        # Validate that file_size_in_bytes is coercible to a positive number greater than
        # or equal to FILE_SIZE_MINIMUM_BYTES
        if file_size_in_bytes < FILE_SIZE_MINIMUM_BYTES:
            raise ValueError(
                f"Parameter 'file_size_in_bytes [long]' must be at least {FILE_SIZE_MINIMUM_BYTES}"
            )

        # Validate that column_names has been provided and is a list
        if not column_names:
            raise ValueError("Parameter 'column_names [list of strings]' is required")
        if not type(column_names) == list:
            raise ValueError("Parameter 'column_names' must be a list of strings")

        self._verbose_output = verbose_output if verbose_output else False
        self._xml_file_object = xml_file_object
        self._file_size_in_bytes = file_size_in_bytes

        self._status_update_frequency_bytes = (
            status_update_frequency_bytes
            if status_update_frequency_bytes
            else file_size_in_bytes / 1000
        )

        self._content_direct_parent = (
            content_direct_parent if content_direct_parent else "seg"
        )

        self._content_row_divider = content_row_divider if content_row_divider else "tu"
        self._content_column_names = column_names
        self._content_column_names_len = len(self._content_column_names)
        self._write_row = (
            write_row
            if write_row
            else lambda values, column_names: print(values, column_names)
        )

        # Store iteratively each current piece of content (to be written when content_row_divider is closed)
        self._current_values = []

        if self._experimental:
            # Currently not used, experimental only. An array built by creating a new current_element_parents
            # beginning with the currently-starting element, and followed by all previously currently-starting
            # elements in antichronological order.
            self._current_element_parents = []

        # Signal to the characters() method that content should be saved into self._current_values
        # ultimately to be written when the end of the current content_row_divider element is encountered
        self._is_content = False

        # Used internally to keep track of when another status update should happen (adds the value supplied
        # in self._status_update_frequency_bytes each time the status is updated and awaits that number of
        # bytes or more for the next iterative update)
        self._next_status_update_threshold = 0

        if self._verbose_output:
            print(vars(self))

        super(TMXColumnParser, self).__init__()

    def startDocument(self):
        if self._verbose_output:
            print(f"Starting parse on '{self._xml_file_object.name}'...")
        super(TMXColumnParser, self).startDocument()

    def endDocument(self):
        if self._verbose_output:
            print(f"Parse finished on on '{self._xml_file_object.name}'...")
        super(TMXColumnParser, self).endDocument()

    # Event fired when an XML element starts
    def startElement(self, name, attrs):
        if self._verbose_output:
            print(f"opening element: {name}")

        self._starting_element = name

        if self._experimental:
            # Experimental code only. self._current_element_parents is not used, but may be used
            # in a future enhancement to deal with deep hierarchies
            self._current_element_parents.insert(
                0, {"name": self._starting_element, "attrs": attrs}
            )

        if self._starting_element == self._content_direct_parent:
            # Always ensure self._current_values[current_idx] defaults to an empty string
            self._current_values.append("")

            # Let characters() method know that any characters accepted until further notice
            # should be considered content
            self._is_content = True

        super(TMXColumnParser, self).startElement(name, attrs)

    # Event fired when an XML element ends
    def endElement(self, name):
        if self._verbose_output:
            print(f"closing element: {name}")

        if self._experimental:
            # Experimental only (not used):
            # Remove the most recent entry from the hierarchy of elements
            test_closing_element = self._current_element_parents.pop(0)

            # Experimental only (not used):
            if not closing_element == test_closing_element["name"]:
                raise ValueError(
                    f"Expected closing element '{test_closing_element}' popped from current_element_parents stack to equal actual closing element '{closing_element}'"
                )

        closing_element = name

        # If a content direct parent element is closing, signal to the characters() method that viable content
        # is not currently available
        if closing_element == self._content_direct_parent:
            self._is_content = False

        # If a content divider element is closing, write the content element using the supplied write_row lambda
        # and set stack of current values back to an empty array
        if closing_element == self._content_row_divider:
            self._write_row(self._current_values)
            self._current_values = []

        """
        
        Show status bar every time self._status_update_frequency_bytes number of bytes are eclipsed

        """
        current_file_position_bytes = self._xml_file_object.tell()

        if (
            self._status_update_frequency_bytes > 0
            and current_file_position_bytes > self._next_status_update_threshold
        ):
            self._next_status_update_threshold += self._status_update_frequency_bytes

            # parameter 'end' causes it to print to the same line if not being interrupted by other console logs
            print(
                f"Status: {current_file_position_bytes / self._file_size_in_bytes * 100:.2f}%\r",
                end="",
            )

        super(TMXColumnParser, self).endElement(name)

    # Event fired once for every element regardless of content
    def characters(self, content):
        if self._is_content and self._starting_element == self._content_direct_parent:
            # This is a potentially desired piece of content.

            # We should only adding content to the last element in the array
            current_idx = len(self._current_values) - 1

            if self._verbose_output:
                print(f"content of current element: {content}")
                print(f"current_idx: {current_idx}")

            # Check if current column index is out of bounds of the self._content_column_names array
            if current_idx >= self._content_column_names_len:
                raise ValueError(
                    f"Input TMX file is malformed or your parameters to your instance of {type(self).__name__ } are not representative of the data elements contained in your TMX file."
                )

            # Concatenate any new content with the existing self._current_values[...]
            if content:
                self._current_values[current_idx] += content

        super(TMXColumnParser, self).characters(content)


"""
parse_tmx_xml_file_object

Functional wrapper for TMXColumnParser. Uses defaults of TMXColumnParser
unless overriden

"""


def parse_tmx_xml_file_object(
    xml_file_object,
    file_size_in_bytes,
    verbose_output=None,
    status_update_frequency_bytes=None,
    write_row=None,
    column_names=None,
    content_direct_parent=None,
    content_row_divider=None,
    experimental=None,
):
    content_handler = TMXColumnParser(
        xml_file_object,
        file_size_in_bytes,
        verbose_output=verbose_output,
        status_update_frequency_bytes=status_update_frequency_bytes,
        column_names=column_names,
        write_row=write_row,
        content_direct_parent=content_direct_parent,
        content_row_divider=content_row_divider,
        experimental=experimental,
    )
    try:
        parse(xml_file_object, content_handler)
    except SAXParseException as err:
        print("Error during SAX parsing:", err)


"""
LIMITATION: As of right now, this only works for TMX files when specifying ALL of the column_names
in the file. To get a select range of column indices, or even better a select list of language
abbreviations, some enhancements will need to be made, but this works to get a basic TMX file
in its entirety over to CSV or perform some other iterative parsing action.

Parses any TMX file according to a lambda that defines what needs to happen when a row (dict)
is written (either to CSV file, to console, or to in-memory structure like dataframe).

"""


def parse_tmx_file(
    tmx_filepath,
    column_names,
    write_row=None,
    verbose_output=None,
    # Override these to customize how the TMX (XML) file is parsed if wanting to use
    # the parser in a different way
    status_update_frequency_bytes=None,
    content_direct_parent=None,
    content_row_divider=None,
):
    with open(tmx_filepath) as file:
        parse_tmx_xml_file_object(
            file,
            file_size_in_bytes=os.stat(tmx_filepath).st_size,
            column_names=column_names,
            write_row=write_row,
            verbose_output=verbose_output,
            status_update_frequency_bytes=status_update_frequency_bytes,
            content_direct_parent=content_direct_parent,
            content_row_divider=content_row_divider,
        )
