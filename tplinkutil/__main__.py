import sys

from tplinkutil import logger, tputil, config
from tplinkutil.modes import circadian


def main():
    args = config.get()
    if args.circadian:
        sun = circadian.Sun(args.lat, args.long)
        tp = tputil.TPUtil(circadian.Circadian(sun, args.timestep))

    if args.music:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    if args.joystick:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    tp.run()


main()
