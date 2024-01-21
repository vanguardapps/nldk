def get_basic_object():
    """
    Literally just get an object that you can use like `object.some_key = 3`.
    This should not be this obtuse. JavaScript is far superior with things
    like this.
    """
    return type("basic_object", (object,), {})()
