# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

- Text lemmatization in non-English languages.
- Static documentation for `run.py` CLI tool.

## [0.0.1-alpha.0] - 2024-01-21

### Added

- `all_languages`: All languages list.
- `clean_content_file`: Clean unicode text content file with option flags for most common NLP text cleaning operations. Uses `NLPContentCleaner` as backend.
- `content_cleaner_languages_supported()`: Get languages supported by selected feature flags for `NLPContentCleaner` instnace or single usage of `clean_content_file()`.
- `get_basic_object()`: Internal use. Basic object generator.
- `CLIMenu (class)`: Create quick CLI tools.
- `load_nltk`: Internal use. Load required NLTK resources using their download utility.
- `NLPContentCleaner (class)`: Backend for `clean_content_file()`. Contains option flags for most common NLP text cleaning operations.
- `parse_tmx_file()`: Parse standard multilingual TMX files and perform operation iteratively. Works well for very large TMX files with low memory footprint.
- `print_file_lines()`: Retrieve and output a subset of lines from a (usually large) file.
- `nldk (CLI tool)`: Runs the CLI version of this kit. One-stop CLI utility for cleaning large content sources, converting large content files, and performing common NLP preprocessing tasks. Use `nldk --help` for usage documentation.
- `TMXColumnParser (class)`: Configurable backend for `parse_tmx_file()` utility function.
- `tmx2csv()`: Convert standard multilingual TMX file to CSV. Allows on-the-fly cleaning using `NLPContentCleaner` class.
- `tsv2csv()`: Convert TSV (tab-separated value) file to CSV (comma-separated value) file.
- `write_csv_line():`: Internal use. Write one line in properly-escaped CSV format to an existing (and open) file object.

[unreleased]: https://github.com/vanguardapps/nldk/tree/dev

[0.1.0-alpha.0]: _TODO: add link to github tag_
