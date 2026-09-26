from .write_through_cache import PickleDatabase


class Database(PickleDatabase):
    def __init__(self, filepath: str = "database.pkl") -> None:
        super().__init__(filepath)
