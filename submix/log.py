import logging
from . import color


# loggers/handlers/formatters are configured in settings.LOGGING
base_lg = logging.getLogger('submix')


# Log format derived from: '[%(name)s] %(levelname)s %(message)s t=%(asctime)s p=%(pathname)s:%(lineno)d'
class ColorfulFormatter(logging.Formatter):
    log_prefix = '%(asctime)s %(levelname)s %(name)s'
    log_suffix = '[%(funcName)s]'
    prefix_color_map = {
        logging.DEBUG: color.cyan,
        logging.INFO: color.blue,
        logging.WARN: color.yellow,
        logging.ERROR: color.red,
        logging.FATAL: color.red_bg,
    }
    suffix_color = [color.grayscale[10]]  # avoid method binding

    def __init__(self):
        super().__init__(datefmt='%Y-%m-%dT%H:%M:%S')

    def usesTime(self):
        """Because we don't set fmt for the base class formatter,
        which the `format()` method uses to determine `record.asctime`,
        override to always return True.
        """
        return True

    def formatMessage(self, record):
        prefix_color = self.prefix_color_map.get(record.levelno, color.cyan)
        s = prefix_color(self.log_prefix % record.__dict__) + ' ' \
            + record.message + ' ' \
            + self.suffix_color[0](self.log_suffix % record.__dict__)
        return s
