import os
import pickle


class PickleDatabase:
    """Pickle database with Copy-on-Write / Write through Cache to handle persistant data with fast query times"""

    def __init__(self, filepath: str = "database.pkl") -> None:
        self.filepath = filepath
        self._data = {}
        self._load()

    def _load(self):
        """Read from file on init if the file exists"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "rb") as f:
                    self._data = pickle.load(f)
            except EOFError, pickle.UnpicklingError:
                # Handle corrupted or empty files gracefully
                self._data = {}

    def _write_to_disk(self):
        """Write current database to file"""
        with open(self.filepath, "wb") as f:
            pickle.dump(self._data, f)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __getitem__(self, key) -> None:
        self.get(key)

    def set(self, key, value):
        self._data[key] = value
        self._write_to_disk()

    def __setitem__(self, key, value) -> None:
        self.set(key, value)

    def delete(self, key):
        if key in self._data:
            del self._data[key]
            self._write_to_disk()

    def __delitem__(self, key):
        self.delete(key)
