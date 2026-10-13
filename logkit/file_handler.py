import logging
from logging.handlers import RotatingFileHandler

_FORMAT = "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def make_file_handler(path, level, max_bytes, backup_count):
    """Writes log lines to `path`, e.g. `2026-10-13 14:02:07.123 [INFO] main: started`.

    When the file reaches max_bytes it is renamed to app.log.1 (the old .1
    becomes .2, and so on) and a fresh file is started. Only backup_count
    old files are kept.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_FORMAT, _DATE_FORMAT))
    return handler
