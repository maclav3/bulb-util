import argparse
import sys

from . import logger


def main():
    parser = argparse.ArgumentParser(
        description='An util to control TP-link smart bulbs. .'
    )

    modes = parser.add_argument_group('Choose at list one from the listed modes')
    modes.add_argument('-c', '--circadian', action='store_true', help='''This mode strives to simulate the daylight cycle 
    accurately. Use --lat and --long to set the latitude and longitude.''')

    modes.add_argument('-m', '--music', action='store_true', help='''This mode turns the lightbulb into a music visualization, 
    based on the system audio output.''')

    modes.add_argument('-j', '--joystick', action='store_true', help='''This mode turns a joystick into the light controller, 
    binding two axes to hue and one axis to brightness.''')

    circadianOpts = parser.add_argument_group('options for circadian mode')

    circadianOpts.add_argument('--longitude', '--long', dest='long', type=float, help='''Set the longitude for daylight simulation. 
    Ranges from -180.0 (Western hemisphere) to +180.0 (Eastern hemisphere). Defaults to the device's current longitude''')

    circadianOpts.add_argument('--latitude', '--lat', dest='lat', type=float, help='''Set the latitude for daylight simulation. 
    Ranges from -90.0 (Southern hemisphere) to +90.0 (Northern hemisphere). Defaults to the device's current latitude''')

    parser.add_argument('--timestep', type=float, default=0, help='''Set the timestep for changing the lighting.''')

    args = parser.parse_args()

    modesChosen = 0 + args.circadian + args.music + args.joystick
    if not modesChosen == 1:
        logger.error('You have to choose at least one mode')
        sys.exit(1)

    if args.circadian:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    if args.music:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    if args.joystick:
        logger.info('Not implemented yet, sorry')
        sys.exit(2)

    sys.exit(0)


main()
