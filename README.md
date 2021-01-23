# image_convert

Python script to make it easy to do a few simple image manipulations.  Mostly done so that I could convert dark images to light images with white backgrounds to save ink when I print them.  Best for dark mode apps with text.



### Syntax

```
python image_convert.py [ [ -commands ] filenames ]+
```

| Option    | Description                                                  |
| --------- | ------------------------------------------------------------ |
| filenames | space-separated and/or wildcarded filenames                  |
| commands  | comma-separated list (no embedded spaces) of command to apply to the following files (details below) |


 		

### Details

| Command   | Description                                                  |
| --------- | ------------------------------------------------------------ |
| i         | invert the image                                             |
| t*NNN*    | threshold for low intensity.  'NNN' is a number from 0 to 255. For example if *NNN* were 32, then all pixels which had an intensity of less than or equal to 32 would be set to 0 (black). |
| b*HHHHHH* | background color.  *HHHHHH* is a triplet of hexadecimal characters representing the RGB values of the background.  For example: b000000 would be black and bFFFFFF would be white.  This is used if it is necessary to handle (semi-)transparency. |
| h,?       | prints help text                                             |



### Examples

    * To invert an image
    python image_convert.py -i image.png
    
    * To force dark colors to black:
    python image_convert.py -t32 image.png
    
    * To force light colors to white:
    python image_convert.py -i,t32,i image.png
    
    * To invert one image and force dark colors to black in another
    python image_convert.py -i image1.png -t32 image2.png
    
    * To invert all images
    python image_convert.py - i *.png *.jpg

### Note

Only tested for PNG and JPG files. Converted files lose their transparency.