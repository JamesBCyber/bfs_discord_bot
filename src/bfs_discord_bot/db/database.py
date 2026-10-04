from .write_through_cache import JsonDatabase


class Database(JsonDatabase):
    """Write through cache database. Only init once to avoid mixed writes and desync the database"""

    def __init__(self, filepath: str = "database.json") -> None:
        """init the database with dummy values if reading from file fails or doesnt load the correct content"""
        super().__init__(filepath)


database = Database()
