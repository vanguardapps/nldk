import os, sys


def relative_path(filepath):
    """
    Get relative path with respect to whatever file the calling code is in.
    """
    caller__file__ = sys._getframe(1).f_globals["__file__"]
    caller_dirname = os.path.dirname(caller__file__)
    return os.path.join(caller_dirname, filepath)
