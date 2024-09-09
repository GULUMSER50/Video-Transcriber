import os

def ensure_dir(file_path):
    """Ensure that a directory exists."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_extension(file_path):
    """Get the file extension of a given file path."""
    return os.path.splitext(file_path)[1]
