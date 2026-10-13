import logging
import os
from pathlib import Path

from .console_handler import make_console_handler
from .exception_hooks import hook_exceptions
from .file_handler import make_file_handler

# Third-party loggers that drown everything else at DEBUG.
_DEFAULT_QUIET = {"httpcore": logging.WARNING, "hpack": logging.WARNING}

_configured = False


def setup(
    log_dir="logs",
    filename="app.log",
    debug=False,
    console_level=None,
    file_level=logging.DEBUG,
    max_bytes=10_000_000,
    backup_count=10,
    quiet=None,
    console_quiet=None,
    color=None,
):
    """Configure root logging once. Safe to call repeatedly.

    log_dir / filename -- file log location; a relative log_dir is resolved
                          against the current working directory.
    debug              -- console shows DEBUG instead of INFO.
    console_level      -- overrides `debug` for the console.
    file_level         -- the file keeps everything (DEBUG) by default, even
                          when the console is quiet.
    quiet              -- silence a noisy library completely: neither the
                          console nor the file gets its messages, except the
                          ones at the given level or more serious.
                          Example: {"httpcore": logging.WARNING}
                          (httpcore and hpack are already set this way).
    console_quiet      -- same, but only for the console. The file still
                          gets everything.
                          Example: {"httpx": logging.WARNING} keeps httpx's
                          request lines in the file but off the screen.
    color              -- force colors on/off; default: on if FORCE_COLOR is
                          set or stdout is a TTY.

    Also routes uncaught exceptions (main thread, threads, asyncio tasks) and
    warnings into the log, so a crash always leaves a trace in the file.
    Returns the log file path.
    """
    global _configured
    path = Path(log_dir) / filename
    if _configured:
        return path

    if console_level is None:
        console_level = logging.DEBUG if debug else logging.INFO

    root = logging.getLogger()
    root.setLevel(min(console_level, file_level))
    _quiet_loggers({**_DEFAULT_QUIET, **(quiet or {})})
    root.addHandler(make_console_handler(console_level, color, console_quiet))
    root.addHandler(make_file_handler(path, file_level, max_bytes, backup_count))

    logging.captureWarnings(True)
    hook_exceptions()

    logging.getLogger(__name__).info(f"Logging to {path.resolve()} (pid={os.getpid()}).")
    _configured = True
    return path


def _quiet_loggers(levels):
    """Raise the minimum level of chatty libraries, e.g. httpcore -> WARNING."""
    for name, level in levels.items():
        logging.getLogger(name).setLevel(level)
