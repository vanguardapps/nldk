class DictCreator(object):
    """
    Create dicts from local variables with just a string list of their names

    Example usage:

    param1 = "value1"
    param2 = "value2"
    param3 = "value3"

    dict_creator = DictCreator(locals())
    my_dict = dict_creator.create_dict("param1", "param2", "param3")
    print(my_dict)

    """

    def __init__(self, your_locals):
        self._your_locals = your_locals

    def create_dict(self, *args):
        result_dict = {}
        for arg in args:
            result_dict[arg] = self._your_locals[arg]
        return result_dict
