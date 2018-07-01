import sys

import configargparse

from bulbutil import logger


def get():
    parser = configargparse.ArgumentParser(
        description='An util to control TP-link smart bulbs.\n',
        default_config_files=('/etc/bulbutil.conf', '~/.config/bulbutil.conf', './bulbutil.conf'),
        args_for_setting_config_path=('--config',)
    )

    modes = parser.add_argument_group('Choose at list one from the listed modes').add_mutually_exclusive_group()
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
        Ranges from -90.0 (Southern hemisphere) to +90.0 (Northern hemisphere). Defaults to the device's current latitude.
        The coordinates are looked up based on the device's IP address.''')

    circadianOpts.add_argument('--min_temperature', type=float, default=2700,
                               help='''The lowest color temperature that will be set during daylight simulation.''')

    circadianOpts.add_argument('--max_temperature', type=float, default=6000,
                               help='''The highest color temperature that will be set during daylight simulation.
                               The color temperature will vary according to the position of the Sun in the sky.''')

    parser.add_argument('--timestep', type=float, default=0, metavar='(mode-dependent)',
                        help='''Set the timestep for changing the lighting.
                        Each mode has a default timestep that is best suited for its operation,
                        but you may override it if you wish.''')

    parser.add_argument('bulb', type=str, help='''The name or IP address of the bulb that is to be controlled.
    Enter 'mock' for a GUI mock bulb, used for testing.
    Enter 'auto' for automatic discovery (not guaranteed to work for all kinds of bulbs).
    
    Otherwise, it is interpreted as the IP address of the bulb.''')

    args = parser.parse_args()

    modesChosen = 0 + args.circadian + args.music + args.joystick
    if not modesChosen == 1:
        logger.error('You have to choose at least one mode')
        sys.exit(1)

    if not args.circadian and (args.long or args.lat):
        parser.error('Coordinates are needed only in circadian mode')

    return args
