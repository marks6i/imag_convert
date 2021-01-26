#!/usr/bin/env python3

from PIL import Image, ImageOps
import sys
import os
from glob import glob
from operator import itemgetter


# global state variables
threshold = 0

def print_help():
    print('''
image_convert - Python script to make it easy to do a few simple image
                manipulations.  Mostly done so that I could convert
                dark images to light images with white backgrounds
                to save ink when I print them.  Best for dark mode apps
                with text.

syntax: python image_convert.py [ [ -<commands> ] <filenames> ]+

        filenames - space-separated and/or wildcarded filenames
        commands  - comma-separated list (no embedded spaces) of commands
                    to apply to the following files. (details below)

details:
    commands:
        i         - invert the image
        tNNN      - threshold for low intensity.  'NNN' is a number from 0
                    to 255. For example if 'NNN' were 32, then all pixels
                    which had an intensity of less than or equal to 32
                    would be set to 0 (black)
        rNNN      - resize by percent. For example, if 'NNN' were 50, the
                    height and width of the image will be halved; if 200,
                    then the height and width would be doubled
        v         - view the current image, possibly in the middle of all
                    transforms
        q,qq      - q(uit) the remaining transforms for the current file ot
                    qq to quit the current and all the remaining transformss
        h,?       - prints this text

examples:

    * To invert an image
    python image_convert.py -i image.png

    * To force dark colors to black:
    python image_convert.py -t32 image.png

    * To force light colors to white:
    python image_convert.py -i,t32,i image.png

    * To invert one image and force dark colors to black in another
    python image_convert.py -i image1.png -t32 image2.png

    * Invert the image and view the image before and after the transform
    python image_convert.py -v,i,v image1.png

    * Halve the dimensions of the image (resize)
    python image_convert.py -r50 image1.png

    *double the dimensions of the image (resize)
    python image_convery.py -r200 image1.png

    * Invert the images and view them but don't save them
    python image_convert.py -i,v,q image1.png image2.png

    * Invert the first image and view it without saving and them stop processing the other images (great for debugging)
    python image_convert.py -i,v,qq image1.png image2.png

    * To invert all images
    python image_convert.py - i *.png *.jpg

note:
    Only tested for PNG and JPG files.
''')


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

        elif command == 'r': # resize image
            try:
                ratio = int(cmd_arg) / 100.0
                if ratio <= 0:
                    print(f"Error: Threshold argument must be greater than 0.", file = sys.stderr)
                    exit(6)
                cmd_list.append([command, ratio])
            except ValueError as ve:
                print(f"Error: command '{command}' only takes an integer argument.", file = sys.stderr)
                exit(7)

        elif command == 'v':
            if not cmd_arg == '':
                print(f"Error: command '{command}' does not take an argument.", file = sys.stderr)
                exit(4)
            cmd_list.append([command, None])

        elif command == 'q':
            if not ( cmd_arg == '' or cmd_arg == 'q' ):
                print(f"Error: command q(q) does not take an argument.", file = sys.stderr)
                exit(5)
            cmd_list.append([command, cmd_arg])

        elif command == 'h' or command == '?': # help screen
            print_help()

        else:
            print(f"Error: command '{command}' is not valid.", file = sys.stderr)
            exit(4)

    return cmd_list


def invert_image(im):
    if im.mode == 'RGBA':
        r, g, b, a = itemgetter(0, 1, 2, 3)(im.split())
        im = Image.merge('RGB', (r, g, b))

        im = ImageOps.invert(im)

        r, g, b    = itemgetter(0, 1, 2)(im.split())
        return Image.merge('RGBA', (r, g, b, a))

    return ImageOps.invert(im)


def _threshold(intensity):
    if intensity <= threshold:
        return 0
    return intensity


def set_threshold(im, level):
    global threshold
    threshold = level
    return im.point(_threshold)


def resize_image(im, ratio):
    image_size = im.size
    width  = image_size[0]
    height = image_size[1]

    new_width  = int(round(width  * ratio))
    new_height = int(round(height * ratio))

    return im.resize((new_width, new_height), Image.LANCZOS)


# ============ main program ================

command_list = []

for arg in sys.argv[1:]:

    if arg[0] == '-':
        commands = arg[1:].lower()
        command_list = set_command(commands)
        continue

    files = glob(arg)

    for filename in files:
        im = Image.open(filename)
        original_format = im.format
        original_mode   = im.mode

        if not ( original_mode == 'RGB' or 
                 original_mode == 'RGBA' ):
            print (f"File '{filename}' cannot be converted, currently image_convert only supports RGB and RGBA.")
            continue

        for cmd in command_list:

            [command, cmd_arg] = cmd

            if   command == 'i': # invert image
                im = invert_image(im)

            elif command == 't': # set threshold
                im = set_threshold(im, cmd_arg)

            elif command == 'r': # set threshold
                im = resize_image(im, cmd_arg)

            elif command == 'v': # view image
                im.show()

            elif command == 'q':
                if (cmd_arg == 'q'):
                    print('Exiting image_convert by command.')
                    exit(0)
                else:
                    break

        if not command == 'q':
            os.rename(filename, filename+'.bak')
            im.save(filename, original_format)
            print(f"File '{filename}' has been converted with command '{commands}'")