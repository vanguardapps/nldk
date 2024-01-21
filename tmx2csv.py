from nlp_content_cleaner import NLPContentCleaner
from tmx import parse_tmx_file
from nlp_content_cleaner import content_cleaner_languages_supported
from all_languages import all_languages
from write_csv_line import write_csv_line


def tmx2csv(
    in_path,
    out_path,
    languages,
    clean_languages=None,
    tmx_verbose_output=None,
    cleaner_verbose_output=None,
    **kwargs,
):
    """
    Converts a multilingual (minimum 1 language) TMX translation file to CSV. Optionally, the output data can be cleaned
    using `NLPContentCleaner`. All of the options available for instantiation of the `NLPContentCleaner` class are
    therefore included in the parameter list for this function.

    @params in_filepath (str): The filepath to the input TMX file
    @params out_filepath (str): The filepath to the output CSV file
    @params languages (str): Space-separated list of languages included in TMX file, full name (ie "english" or "japanese")
    """
    # Remove 'verbose_output' - require user to send `cleaner_verbose_output` explicitly
    if kwargs.get("verbose_output", None):
        del kwargs["verbose_output"]

    languages = languages.split()

    clean_idx2lang = {}
    if clean_languages:
        clean_languages = clean_languages.split()
        for language in clean_languages:
            if not language in languages:
                raise ValueError(
                    f"Language '{language}' specified in `--clean_languages` was not one of the TMX file languages specified by "
                    + "`--languages`. Can only clean language columns that exist in the source TMX file."
                )
            clean_idx2lang[languages.index(language)] = language
        cleaner = NLPContentCleaner(**kwargs)

    print(
        f"Starting conversion{' and cleaning' if clean_languages else ''} of TMX file '{in_path}' to CSV file '{out_path}'..."
    )

    with open(out_path, "w") as csv_file:

        def write_raw_items(items):
            write_csv_line(csv_file, items)

        def write_clean_items(items):
            clean_items = []
            for idx, item in enumerate(items):
                clean_lang = clean_idx2lang.get(idx, None)
                if clean_lang:
                    clean_items.append(
                        cleaner.clean(
                            item, clean_lang, verbose_output=cleaner_verbose_output
                        )
                    )
                else:
                    clean_items.append(item)
            write_csv_line(csv_file, clean_items)

        parse_tmx_file(
            in_path,
            column_names=languages,
            verbose_output=tmx_verbose_output,
            write_row=write_clean_items if clean_languages else write_raw_items,
        )


def tmx2csv_lang_support(**kwargs):
    """
    Given the same parameters that can be passed to tmx2csv(), return an array of language names
    that are supported by the selected features.

    """
    if kwargs.get("clean_languages", None):
        return content_cleaner_languages_supported(**kwargs)
    else:
        return all_languages
