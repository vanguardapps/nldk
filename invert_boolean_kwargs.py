import regex as re


def invert_boolean_kwargs(prefix, kwargs):
    """
    Given a list of kwargs, select the ones that begin with `prefix` and invert the value logically.
    This is intended to be used to convert a parameter like `no_stem` (used by a CLI tool) to the
    affirmative version `stem` automatically.

    @param prefix (str):        The string prefix to look for to determine whether to invert an argument's value
    @param kwargs(Dict):        Dict of keyword arguments to search, copy / update, then return.
    @returns kwargs(Dict):      Returns a copy of kwargs with anything beginning with `prefix` logically inverted.

    NOTE: Currently this is only intended to be used to invert boolean values!
    """

    new_kwargs = {}

    # Logically reverse all keys prefixed with `prefix` (often "no_<affirmative_name>") and store them in kwargs as
    # their "affirmative" counterparts so we can pass them all to the constructor for NLPContentCleaner seamlessly
    for key, value in kwargs.items():
        if key.startswith(prefix):
            new_kwargs[re.sub(f"^{prefix}", "", key)] = not value
        else:
            new_kwargs[key] = value

    return new_kwargs
