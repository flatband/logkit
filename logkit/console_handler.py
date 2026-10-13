import logging
import os
import sys

from .color_formatter import ColorFormatter
from .min_level_filter import MinLevelFilter

_FORMAT = "[%(levelname)s] %(name)s: %(message)s"


def make_console_handler(level, color=None, console_quiet=None):
    """Prints log lines to the terminal, e.g. `[INFO] main: started`.

    Colors are used when the output is a real terminal (or FORCE_COLOR is
    set), not when it goes to a file or pipe.
    """
    if color is None:
        color = bool(os.environ.get("FORCE_COLOR")) or sys.stdout.isatty()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter((ColorFormatter if color else logging.Formatter)(_FORMAT))
    if console_quiet:
        handler.addFilter(MinLevelFilter(console_quiet))
    return handler
