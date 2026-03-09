import sys
import os

def resource_path(relative_path):
    """
    Get the absolute path to a READ-ONLY bundled resource.
    Use this for files included via PyInstaller's --add-data (e.g. bundled WAV files).
    These files are extracted to a temp folder (_MEIPASS) at runtime.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def app_data_path(relative_path):
    """
    Get the absolute path to a WRITABLE file/folder next to the executable.
    Use this for user configs, sfx directories, and anything the app needs to write.
    Unlike _MEIPASS, this location persists between runs and is writable.
    """
    if hasattr(sys, '_MEIPASS'):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.abspath(".")
    return os.path.join(exe_dir, relative_path)