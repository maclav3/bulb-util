import sys

from tplinkutil import logger, tputil, config
from tplinkutil.modes import circadian


def main():
    args = config.get()
    if args.circadian:
        tp = tputil.TPUtil(circadian.Circadian(args.timestep, args.lat, args.long))

    if args.music:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    if args.joystick:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    tp.run()


main()
