# Courtesy http://plumberjack.blogspot.com/2010/12/colorizing-logging-output-in-terminals.html
# Tweaked to use colorama for the coloring

import colorama
import logging
import sys


class ColorizingStreamHandler(logging.StreamHandler):
    color_map = {
        logging.DEBUG: (colorama.Style.DIM + colorama.Fore.CYAN, "*", colorama.Fore.WHITE),
        logging.INFO: (colorama.Fore.WHITE, "*", colorama.Style.BRIGHT + colorama.Fore.GREEN),
        logging.WARNING: (colorama.Fore.YELLOW, "*", colorama.Style.BRIGHT + colorama.Fore.YELLOW),
        logging.ERROR: (colorama.Fore.RED, "!", colorama.Style.BRIGHT + colorama.Fore.RED),
        logging.CRITICAL: (colorama.Back.RED, "!", colorama.Style.BRIGHT + colorama.Fore.RED),
    }

    def __init__(self, stream, color_map=None):
        logging.StreamHandler.__init__(self,
                                       colorama.AnsiToWin32(stream).stream)
        if color_map is not None:
            self.color_map = color_map

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            # Don't colorize a traceback
            parts = message.split('\n', 1)
            parts[0] = self.colorize(parts[0], record)
            message = '\n'.join(parts)
        return message

    def colorize(self, message, record):
        try:
            mc, ch, chc = self.color_map[record.levelno]
            return (colorama.Style.BRIGHT + colorama.Fore.BLUE + '[' +
                    chc + ch + colorama.Style.RESET_ALL +
                    colorama.Style.BRIGHT + colorama.Fore.BLUE + '] ' +
                    colorama.Style.RESET_ALL +
                    mc + colorama.Style.BRIGHT + message +
                    colorama.Style.RESET_ALL)
        except KeyError:
            return message


def get_logger(name):
    handler = ColorizingStreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

logger = logging.getLogger('test')
if __name__ == '__main__':
    handler = ColorizingStreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
