import sys

from tplinkutil import bulbutil, config, logger
from tplinkutil.modes import circadian


def main():
    args = config.get()
    if args.circadian:
        sun = circadian.Sun(args.lat, args.long)
        tp = bulbutil.BulbUtil(circadian.Circadian(sun, args.timestep))

    if args.music:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    if args.joystick:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    tp.run()


main()
