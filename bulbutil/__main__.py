import sys
from pprint import pprint

from bulbutil import bulbutil, config, logger
from bulbutil.bulbs.mock import MockBulb
from bulbutil.bulbs.tplink import TPLink
from bulbutil.exceptions import NoBulbException
from bulbutil.modes import circadian, Mode


def main():
    args = config.get()
    mode = None  # type: Mode

    if args.bulb == 'test':
        bulb = MockBulb()
    else:
        # todo: detect the type of bulb
        if args.bulb == 'auto':
            bulb = TPLink()
        else:
            bulb = TPLink(args.bulb)

    if not bulb:
        raise NoBulbException

    pprint(args)
    if args.circadian:
        sun = circadian.Sun(args.lat, args.long)
        mode = circadian.Circadian(sun, bulb, args.min_temperature, args.max_temperature, args.timestep)

    if args.music:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    if args.joystick:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    tp = bulbutil.BulbUtil(mode)
    tp.run()


main()
