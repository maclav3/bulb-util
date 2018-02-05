import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(pathname)s:%(lineno)d: %(message)s'))

logger = colorlog.getLogger('main')
logger.setLevel('DEBUG')
logger.addHandler(handler)
