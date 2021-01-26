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

| Command | Description                                                  |
| ------- | ------------------------------------------------------------ |
| i       | invert the image                                             |
| t*NNN*  | threshold for low intensity.  'NNN' is a number from 0 to 255. For example if *NNN* were 32, then all pixels which had an intensity of less than or equal to 32 would be set to 0 (black). |
| rNNN    | resize by percent. For example, if 'NNN' were 50, the height and width of the image will be halved; if 200, then the height and width would be doubled |
| v       | view the current image, possibly in the middle of all transforms |
| q,qq    | q(uit) the remaining transforms for the current file or qq to quit the current and all the remaining transforms |
| h,?     | prints help text                                             |



### Examples

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
    python image_convert.py -i *.png *.jpg

### Note

Only tested for PNG and JPG files.
