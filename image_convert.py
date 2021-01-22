from PIL import Image, ImageOps
from icecream import ic
import sys
import os
from glob import glob


# global state variables
background_color = (255, 255, 255)
threshold = 0


def set_command(cmds):
    cmd_list = []
    commands = cmds.split(",")

    # check for errors
    for cmd in commands:

        command = cmd[0]
        cmd_arg = cmd[1:]

        if   command == 'i': # invert image
            if not cmd_arg == '':
                print(f"Error: command '{command}' does not take an argument.", file = sys.stderr)
                exit(1)
            cmd_list.append([command, None])

        elif command == 't': # set threshold
            try:
                thresh = int(cmd_arg)
                if thresh < 0 or thresh > 255:
                    print(f"Error: Threshold argument must be between 0 and 255 inclusive.", file = sys.stderr)
                    exit(2)
                cmd_list.append([command, thresh])
            except ValueError as ve:
                print(f"Error: command '{command}' only takes an integer argument.", file = sys.stderr)
                exit(3)

        elif command == 'b':
            try:
                rgb = tuple(int(cmd_arg[i:i+2], 16) for i in (0, 2, 4))
                cmd_list.append([command, rgb])
            except ValueError as ve:
                print(f"Error: command '{command}' only takes 3 hexdigits as an argument.", file = sys.stderr)
                exit(4)

        elif command == 'h' or command == '?': # help screen
            print('Help!')

        else:
            print(f"Error: command '{command}' is not valid.", file = sys.stderr)
            exit(4)

    return cmd_list


def alpha_to_color(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Source: http://stackoverflow.com/a/9459208/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background
    
    
def invert_image(im):
    if im.mode == 'RGBA':
        im = alpha_to_color(im, background_color)
    return ImageOps.invert(im)


def _threshold(intensity):
    if intensity <= threshold:
        return 0
    return intensity


def set_threshold(im, level):
    global threshold
    threshold = level
    return im.point(_threshold)


def set_background(color):
    global background_color
    background_color = color
    return background_color

# ============ main program ================

command_list = []

for arg in sys.argv[1:]:

    if arg[0] == '-':
        command_list = set_command(arg[1:].lower())
        continue

    files = glob(arg)

    for filename in files:
        im = Image.open(filename)
        original_format = im.format
        original_mode   = im.mode
        ic(filename)
        ic(im.format)
        ic(im.mode)

        for cmd in command_list:

            [command, cmd_arg] = cmd

            if   command == 'i': # invert image
                im = invert_image(im)

            elif command == 't': # set threshold
                im = set_threshold(im, cmd_arg)

            elif command == 'b': # set background for RGBA images
                set_background(cmd_arg)

        os.rename(filename, filename+'.bak')
        im.save(filename, original_format)