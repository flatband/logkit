# logkit

Console + rotating file logging for long-running bots. The file keeps
**everything** (DEBUG, timestamps to the millisecond), so a run killed by the
OOM killer or lost from journald can still be inspected afterwards.

```python
import logging, logkit

logkit.setup(log_dir="logs", filename="ab.log", debug=True,
             console_quiet={"httpx": logging.WARNING})
```

- Console: `[LEVEL] name: message`, colored when a TTY or `FORCE_COLOR` is set.
- File: `<ts> [LEVEL] name: message`, rotated at 10 MB, 10 backups.
- Uncaught exceptions (main, threads, asyncio) and `warnings` land in the log.
- `quiet={...}` caps noisy libraries everywhere; `console_quiet={...}` only
  hides them on screen.

Install: `logkit = { git = "https://github.com/flatband/logkit.git" }`
