import string
import regex as re
import load_nltk

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

content_cleaner_default_language = "english"


class NLPContentCleaner(object):
    def __init__(
        self,
        default_language=None,
        tokenize=None,
        remove_html=None,
        remove_punctuation=None,
        remove_extra_space=None,
        convert_lowercase=None,
        remove_stopwords=None,
        stem=None,
        lemmatize=None,
        lemmatize_pos=None,
    ):
        """
        Constructs a ContentCleaner instance

        @param tokenize (Boolean): Tells the clean() function whether to return the cleaned input as tokens
        or as a whole sentence concatenated again. Defaults to False.

        """
        # Get lists of particular language availability
        self._stopwords_languages = list(stopwords.fileids())
        self._stemmer_languages = list(SnowballStemmer.languages)

        # Until we build a package, we will be limited to lemmatizing in English only
        self._lemmatizer = WordNetLemmatizer()
        self._lemmatizer_languages = ["english"]

        #
        # A Note on the WordNetLemmatizer:
        #
        # Lemmatizer lets you select part of speech!
        # This is really cool, because it means you pick the part of speech to devolve your words into.
        # However, because the lemmatizer currently only supports English, this feature isn't as
        # useful as it would be.
        #
        # This lemmatizer is state of the art (circa 2023), but it is not definitive yet. More work needs to be
        # done in lemmatization to improve data preparation.
        #
        # Example:
        # self._lemmatizer.lematize(word, pos)
        # word (str) – The input word to lemmatize.
        # pos (str) – The Part Of Speech tag. Valid options are “n” for nouns, “v” for verbs, “a” for adjectives,
        # “r” for adverbs and “s” for satellite adjectives.
        #

        # Unless specified, assign default values to options
        self._default_language = (
            default_language if default_language else content_cleaner_default_language
        )
        self._return_tokenized = tokenize if tokenize is not None else False
        self._remove_html = remove_html if remove_html is not None else False
        self._remove_punctuation = (
            remove_punctuation if remove_punctuation is not None else False
        )
        self._remove_extra_space = (
            remove_extra_space if remove_extra_space is not None else False
        )
        self._convert_lowercase = (
            convert_lowercase if convert_lowercase is not None else False
        )
        self._remove_stopwords = (
            remove_stopwords if remove_stopwords is not None else False
        )
        self._stem = stem if stem is not None else False
        self._lemmatize = lemmatize if lemmatize is not None else False

        # Defaults to lemmatizing with the default lemmatizer part of speech
        self._lemmatize_pos = lemmatize_pos if lemmatize_pos is not None else None

    def get_lemmatize_pos_supported(self):
        return (
            {"pos": "n", "meaning": "nouns"},
            {"pos": "v", "meaning": "verbs"},
            {"pos": "a", "meaning": "adjectives"},
            {"pos": "r", "meaning": "adverbs"},
            {"pos": "s", "meaning": "satellite adjectives"},
        )

    def get_languages_supported(self):
        """
        @returns (List[str]): the list of languages that will be supported by the features indicated
            by the parameters of the class instance.
        """
        all_languages = (
            self._stopwords_languages
            + self._stemmer_languages
            + self._lemmatizer_languages
        )
        return list(
            set(self._stopwords_languages if self._remove_stopwords else all_languages)
            & set(self._stemmer_languages if self._stem else all_languages)
            & set(self._lemmatizer_languages if self._lemmatize else all_languages)
        )

    def clean(self, content, language=None, verbose_output=None):
        """
        A series of hand-picked cleanup operations to achieve the following basic results:
        1. Removing HTML characters, ASCII
        2. Remove extra punctuation
        3. Remove extra space characters
        4. Convert to lowercase
        5. Remove stop words
        6. Stem (SnowballStemmer)
        7. Lemmatize (WordNetLemmatizer, only supported for language="english")

        @param content (str): a standard Python unicode string to be cleaned.
        @param language (str): the language that the string is known to be in.
        @param verbose_output(str): display verbose output at each step of cleaning.

        For a list of supported languages, use the get_languages_supported() instance method.
        """

        language = language if language else self._default_language
        verbose_output = verbose_output if verbose_output is not None else False

        if not language:
            raise ValueError(
                "Missing required parameter 'language'. Must be supplied at instantiation time or when calling clean(...)."
            )

        if verbose_output:
            print(f"Content prior to cleaning: {content}")

        # Remove HTML (this is sufficient, but naive. TODO: find more sophisticated / accurate HTML removal)
        if self._remove_html:
            content = re.sub("<.*?>", " ", content)
            if verbose_output:
                print(f"Content after removing html: {content}")

        # Remove all punctuation (kind of a hack of str.maketrans which requires the first two positional
        # parameters, but also adds functionality to remove anything of the type passed in the third, which
        # in this case is string.punctuation)
        if self._remove_punctuation:
            content = content.translate(str.maketrans(" ", " ", string.punctuation))
            if verbose_output:
                print(f"Content after removing punctuation: {content}")

        # Remove any space character including newline with a single space
        if self._remove_extra_space:
            content = re.sub(r"\s+", r" ", content)
            if verbose_output:
                print(f"Content after removing extra space: {content}")

        # Convert to lowercase
        if self._convert_lowercase:
            content = content.lower()
            if verbose_output:
                print(f"Content after converting to lowercase: {content}")

        # Tokenize content
        content = word_tokenize(content)

        if verbose_output:
            print(f"Content after tokenizing: {content}")

        language = language.lower()

        # If language specified and in allowed list of languages, remove stop words (otherwise skip)
        if self._remove_stopwords and language in self._stopwords_languages:
            stop_words = set(stopwords.words(language))
            content = [word for word in content if word not in stop_words]
            if verbose_output:
                print(f"Content after removing stopwords: {content}")

        # Stem content
        if self._stem and language in self._stemmer_languages:
            stemmer = SnowballStemmer(language)
            content = [stemmer.stem(word) for word in content]
            if verbose_output:
                print(f"Content after stemming: {content}")

        # Lemmatize content (supports only English at this time)
        # TODO: write or find package for multilingual lemmatization (have not found one yet)
        if self._lemmatize and language in self._lemmatizer_languages:
            if self._lemmatize_pos is not None:
                content = [
                    self._lemmatizer.lemmatize(word, self._lemmatize_pos)
                    for word in content
                ]
            else:
                content = [self._lemmatizer.lemmatize(word) for word in content]
            if verbose_output:
                print(f"Content after lemmatization: {content}")

        return content if self._return_tokenized else " ".join(content)


def get_lemmatize_pos_supported():
    cleaner = NLPContentCleaner()
    return cleaner.get_lemmatize_pos_supported()


def content_cleaner_languages_supported(**kwargs):
    """
    Returns the languages supported by the supplied feature set, using NLPContentCleaner class
    defaults when parameter not supplied.

    NOTE: Only these three options have any effect on language suppport, which is why the other
    initialization options have been left out.

    @param **kwargs:
        See below

    Keyword Arguments:
        'remove_stopwords' (Boolean): Include stopword removal in the list of features for which supported
        languages are returned.
        'stem' (Boolean): Include stemming in the list of features for which supported languages are returned.
        'lemmatize' (Boolean): Include lemmatization in the list of features for which supported languages
        are returned.
        NOTE: All other arguments of NLPContentCleaner are accepted, but have no effect on language support.

    @returns (List[str]): the list of languages that will be supported by the features indicated
        by the boolean parameters above. I"f none are supplied, it is assumed a list of languages
        supported by all features is desired.
    """
    remove_stopwords = kwargs.get("remove_stopwords", None)
    stem = kwargs.get("stem", None)
    lemmatize = kwargs.get("lemmatize", None)

    cleaner = NLPContentCleaner(
        remove_stopwords=remove_stopwords, stem=stem, lemmatize=lemmatize
    )

    return cleaner.get_languages_supported()


def clean_content_file(
    in_path,
    out_path,
    language=None,
    tokenize=None,
    remove_html=None,
    remove_punctuation=None,
    remove_extra_space=None,
    convert_lowercase=None,
    remove_stopwords=None,
    stem=None,
    lemmatize=None,
    lemmatize_pos=None,
    verbose_output=None,
):
    cleaner = NLPContentCleaner(
        default_language=language,
        tokenize=tokenize,
        remove_html=remove_html,
        remove_punctuation=remove_punctuation,
        remove_extra_space=remove_extra_space,
        convert_lowercase=convert_lowercase,
        remove_stopwords=remove_stopwords,
        stem=stem,
        lemmatize=lemmatize,
        lemmatize_pos=lemmatize_pos,
    )

    with open(in_path, "r") as input_file:
        with open(out_path, "w") as output_file:
            for line in input_file:
                output_file.write(
                    cleaner.clean(content=line, verbose_output=verbose_output)
                )
    print(
        f"Finished cleaning '{language if language else content_cleaner_default_language}' language input file '{in_path}'. Clean output written to file '{out_path}'"
    )

    """
    Th above call to cleaner.clean executes a series of hand-picked cleanup operations
    to achieve the following basic results:
        1. Removing HTML characters, ASCII
        2. Remove extra punctuation
        3. Remove extra space characters
        4. Convert to lowercase
        5. Remove stop words
        6. Stem (SnowballStemmer)
        7. Lemmatize (WordNetLemmatizer, only supported for language="english")

    @param content (str): a standard Python unicode string to be cleaned.
    @param language (str): the language that the string is known to be in.
    @param verbose_output(str): display verbose output at each step of cleaning.

    For a list of supported languages, use the get_languages_supported() function.
    """
