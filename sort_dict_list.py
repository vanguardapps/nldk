def sort_dict_list(list_of_dicts, key, reverse=False):
    """
    Sorts a list of dicts by a particular string key in each of the dicts. Assumes passed-in dict key to be
    present on all dicts in the list. reverse=True for descending order.
    """
    return sorted(list_of_dicts, key=lambda d: d[key], reverse=reverse)
