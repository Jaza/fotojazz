import Image


# Code borrowed from:
# http://flask.pocoo.org/mailinglist/ \
# archive/2011/1/26/pil-to-create-thumbnails- \
# automatically-using-tag/#32aff91e05ba9985a49a76a4fb5338d7
def resize(img, box, fit, out, quality=75):
    '''Downsample the image.

    script example :
     >>> import Image, os, sys
     >>> for filename in sys.argv[1:]:
     >>>     img = Image.open(filename).resize( (200,200) )
     >>>     out = file(os.path.splitext(filename)[0]+"_thumb.jpg", "w")
     >>>     try:
     >>>         img.save(out, "JPEG")
     >>>     finally:
     >>>         out.close()

    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
    @param out: file-like-object - save the image into the output stream
    '''
    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
        factor *= 2
    if factor > 1:
        img.thumbnail((img.size[0] / factor, img.size[1] / factor),
                      Image.NEAREST)

    #calculate the cropping box and get the cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / box[0]
        hRatio = 1.0 * y2 / box[1]
        if hRatio > wRatio:
            y1 = y2 / 2-box[1] * wRatio / 2
            y2 = y2 / 2 + box[1] * wRatio / 2
        else:
            x1 = x2 / 2-box[0] * hRatio / 2
            x2 = x2 / 2 + box[0] * hRatio / 2
        img = img.crop((x1, y1, x2, y2))

    #Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)

    #save it into a file-like object
    img.save(out, "JPEG", quality=75)
