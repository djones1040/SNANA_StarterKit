"""
I/O utilities
"""
import gzip
import pickle


def save_compressed(data, path):
    """
    Save as compressed pickle file.

    The use of `protocol=2` in the pickling of the files ensures
    data can be unpickled from both Python 2 and 3

    Parameters
    ----------
    data : object
        Python object to save
    path : str or Path
        filename to save the data to

    """
    with gzip.open(path, 'wb') as output:
        pickle.dump(data, output, protocol=2)


def read_compressed(path):
    """
    Read the compressed pickle file

    Parameters
    ----------
    path : str or Path
        filename to save the data to

    Returns
    -------
    Python object unpickled

    """
    with gzip.open(path, 'rb') as f:
        data = pickle.load(f)

    return data
