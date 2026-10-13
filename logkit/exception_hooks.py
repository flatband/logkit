import asyncio
import logging
import sys
import threading

_log = logging.getLogger("uncaught")


def hook_exceptions():
    """Make crashes get written to the log, not only printed on screen."""
    _hook_main_thread()
    _hook_threads()
    _hook_asyncio()


def _hook_main_thread():
    """An error nobody catches stops the program. Python then calls
    sys.excepthook to print it; ours logs it instead. Ctrl+C is left alone."""

    def excepthook(exc_type, exc, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc, tb)
            return
        _log.critical("Uncaught exception", exc_info=(exc_type, exc, tb))

    sys.excepthook = excepthook


def _hook_threads():
    """Same idea, for a background thread that dies from an error."""

    def thread_hook(args):
        _log.critical(
            f"Uncaught exception in thread {args.thread.name if args.thread else '?'}",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    threading.excepthook = thread_hook


def _hook_asyncio():
    """Same idea, for asyncio. An error in a task nobody awaits never reaches
    sys.excepthook; asyncio hands it to the event loop's exception handler
    instead. asyncio.run() creates its loop with new_event_loop(), so we
    replace that function with one that also installs our handler."""
    original_new_event_loop = asyncio.events.new_event_loop

    def handler(loop, context):
        exc = context.get("exception")
        _log.error(
            context.get("message", "asyncio error"),
            exc_info=(type(exc), exc, exc.__traceback__) if exc else None,
        )

    def new_event_loop():
        loop = original_new_event_loop()
        loop.set_exception_handler(handler)
        return loop

    asyncio.events.new_event_loop = new_event_loop
    asyncio.new_event_loop = new_event_loop
