import logging

class MinLevelFilter(logging.Filter):
    """Console-only: hide records of the given loggers below a level.

    Done as a handler filter (not by mutating the record) so the file
    handler still receives the record untouched.
    """

    def __init__(self, levels: dict):
        super().__init__()
        self.levels = levels

    def filter(self, record):
        for name, level in self.levels.items():
            if record.name == name or record.name.startswith(name + "."):
                return record.levelno >= level
        return True