from nlp_content_cleaner import (
    clean_content_file,
    content_cleaner_languages_supported,
    get_lemmatize_pos_supported,
)
from cli_menu import CLIMenu
from tmx2csv import tmx2csv, tmx2csv_lang_support
from all_languages import all_languages
from tsv2csv import tsv2csv
from print_file_lines import print_file_lines


def cli_clean_content_file(
    cleaner_verbose_output=None,
    **kwargs,
):
    # Remove 'verbose_output' - require user to send `cleaner_verbose_output` explicitly
    if kwargs.get("verbose_output", None):
        del kwargs["verbose_output"]

    if cleaner_verbose_output:
        kwargs["verbose_output"] = cleaner_verbose_output

    clean_content_file(**kwargs)


if __name__ == "__main__":
    menu = CLIMenu()

    menu.add_primary_flag(
        flag="tsv2csv",
        help="Convert a file with tab-separated values (TSV) to a file with comma-separated values (CSV).",
        callback=tsv2csv,
        get_languages_supported=lambda: all_languages,
        required_params={
            "in_path": "The path to the tab-separated values (TSV) file.",
            "out_path": "The path to the comma-separated values (CSV) file.",
        },
    )

    menu.add_primary_flag(
        flag="print_file_lines",
        help="Retrieve a select range of lines from a (usually large) file.",
        callback=print_file_lines,
        get_languages_supported=lambda: all_languages,
        required_params={
            "in_path": "The path to the input file.",
            "start_line": "The integer line number on which to begin reading lines.",
            "end_line": "The integer line number on which to end reading lines.",
            "out_path": "The path to the output file.",
        },
    )

    menu.add_primary_flag(
        flag="tmx2csv",
        help="Convert a multi-lingual TMX file to a standard CSV file. Specify `--clean_languages spanish japanese` to clean select language "
        + "output on conversion to CSV. All options from `--clean_content_file` primary utility also apply to cleaning if `--clean_languages` specified.",
        callback=tmx2csv,
        get_languages_supported=tmx2csv_lang_support,
        required_params={
            "in_path": "The path to the multilingual TMX file.",
            "out_path": "The path to the CSV file to be created/overwritten.",
            "languages": "A space-separated list of all lowercase languages (full names) in TMX column order enclosed in quotes. "
            + 'Ex: `--languages "english spanish japanese"`. '
            + "Should be the full list of languages included in TMX file.",
        },
        optional_params={
            "clean_languages": "A space-separated list of all lowercase languages (full names) enclosed in quotes to clean the output of "
            + 'prior to writing to CSV. NOTE: No output will be cleaned unless `--clean_languages` is specified. Ex: `--clean_languages "spanish japanese"`. ',
            "tokenize(bool)": "Tokenize the cleaned content before outputing. Defaults to False. "
            + "Prints a list of list of strings created using `nltk.tokenize.word_tokenize`. "
            + "This kind of tokenization is not as effective with Eastern languages. Recommended for "
            + "European-origin, space-separated languages only.",
            "remove_html(bool)": "Remove stray HTML tags in the content. Defaults to False. HTML removal uses RegEx s/<.*?>//g to accomplish this.",
            "remove_punctuation(bool)": "Remove all punctuation. Defaults to False.",
            "remove_extra_space(bool)": "Remove all extra spaces. Defaults to False. Specifically, any number of space characters "
            + "(spaces, newlines, etc) are replaced by a single horizontal space unless this flag is specified.",
            "convert_lowercase(bool)": "Convert clean content to lowercase. Defaults to False.",
            "remove_stopwords(bool)": "Remove stopwords from content. Defaults to False. Stopword removal uses `nltk.corpus.stopwords` "
            + "parameterized by cleaner instance `--language`. NOTE: Stopword removal only works for certain languages. Use the "
            + "`--languages_supported` flag in conjunction with your desired run configuration to see what languages "
            + "suppport your combination of feature flags.",
            "stem(bool)": "Stem the content word by word according to the passed `--language`. Defaults to False. NOTE: "
            + "Stemming only works for certain languages. Use the `--languages_supported` flag in conjunction "
            + "with your desired run configuration to see what languages suppport your combination (or non-use) of feature flags.",
            "lemmatize(bool)": "Lemmatize the content word by word according to the passed `--language`. Defaults to False. Lemmatizer uses "
            + "`nltk.stem.wordnet.WordNetLemmatizer` under the hood. NOTE: Lemmatizing only works for "
            + "`--language english` due to the `WordNetLemmatizer`. Fixing this limitation is high priority with the NLDK devs.",
            "lemmatize_pos": "Change the part of speech returned by the lemmatizer. Uses `nltk.stem.wordnet.WordNetLemmatizer` default part of speech "
            + f"by default. Options are {get_lemmatize_pos_supported()}",
            "cleaner_verbose_output(bool)": "Enable verbose content cleaner output to the console. File specified with `--out_path` will also be written. "
            + "Defaults to False. For large content, pipe stdout to a file with `... > your_file.output`. Verbose output includes step-wise cleaning of "
            + "each line, which can be helpful for debugging.",
            "tmx_verbose_output(bool)": "Enable verbose TMX parser output to the console. File specified with `--out_path` will also be written. "
            + "Defaults to False. For large content, pipe stdout to a file with `... > your_file.output`. Verbose output includes step-wise cleaning of "
            + "each line, which can be helpful for debugging.",
        },
    )

    menu.add_primary_flag(
        flag="clean_content_file",
        help="Perform a series of standard preprocessing steps to clean/prepare the content of a unicode text file.",
        callback=cli_clean_content_file,
        get_languages_supported=content_cleaner_languages_supported,
        required_params={
            "in_path": "The path to the raw file.",
            "out_path": "The path to the cleaned file to be created/overwritten.",
        },
        optional_params={
            "language": "The language of the raw file (full name and lowercase: like 'spanish' or 'japanese') . ",
            "tokenize(bool)": "Tokenize the cleaned content before outputing. Defaults to False. "
            + "Prints a list of list of strings created using `nltk.tokenize.word_tokenize`. "
            + "This kind of tokenization is not as effective with Eastern languages. Recommended for "
            + "European-origin, space-separated languages only.",
            "remove_html(bool)": "Remove stray HTML tags in the content. Defaults to False. HTML removal uses RegEx s/<.*?>//g to accomplish this.",
            "remove_punctuation(bool)": "Remove all punctuation. Defaults to False.",
            "remove_extra_space(bool)": "Remove all extra spaces. Defaults to False. Specifically, any number of space characters "
            + "(spaces, newlines, etc) are replaced by a single horizontal space unless this flag is specified.",
            "convert_lowercase(bool)": "Convert clean content to lowercase. Defaults to False.",
            "remove_stopwords(bool)": "Remove stopwords from content. Defaults to False. Stopword removal uses `nltk.corpus.stopwords` "
            + "parameterized by cleaner instance `--language`. NOTE: Stopword removal only works for certain languages. Use the "
            + "`--languages_supported` flag in conjunction with your desired run configuration to see what languages "
            + "suppport your combination of feature flags.",
            "stem(bool)": "Stem the content word by word according to the passed `--language`. Defaults to False. NOTE: "
            + "Stemming only works for certain languages. Use the `--languages_supported` flag in conjunction "
            + "with your desired run configuration to see what languages suppport your combination (or non-use) of feature flags.",
            "lemmatize(bool)": "Lemmatize the content word by word according to the passed `--language`. Defaults to False. Lemmatizer uses "
            + "`nltk.stem.wordnet.WordNetLemmatizer` under the hood. NOTE: Lemmatizing only works for "
            + "`--language english` due to the `WordNetLemmatizer`. Fixing this limitation is high priority with the NLDK devs.",
            "lemmatize_pos": "Change the part of speech returned by the lemmatizer. Uses `nltk.stem.wordnet.WordNetLemmatizer` default part of speech "
            + f"by default. Options are {get_lemmatize_pos_supported()}",
            "cleaner_verbose_output(bool)": "Enable verbose content cleaner output to the console. File specified with `--out_path` will also be written. "
            + "Defaults to False. For large content, pipe stdout to a file with `... > your_file.output`. Verbose output includes step-wise cleaning of "
            + "each line, which can be helpful for debugging.",
        },
    )

    menu.execute()
