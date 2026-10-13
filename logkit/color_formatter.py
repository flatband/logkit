import logging

class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

    def format(self, record):
        msg = super().format(record)
        if record.levelno >= logging.ERROR:
            return f"{self.RED}{msg}{self.RESET}"
        if record.levelno >= logging.WARNING:
            return f"{self.YELLOW}{msg}{self.RESET}"
        if record.levelno >= logging.INFO:
            return f"{self.BLUE}{msg}{self.RESET}"
        return msg