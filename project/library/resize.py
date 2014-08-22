from PIL import Image
from StringIO import StringIO


def resize(file, width, height, crop, quality=75):
    '''Code borrowed (with modifications) from:
    http://flask.pocoo.org/mailinglist/ \
    archive/2011/1/26/pil-to-create-thumbnails- \
    automatically-using-tag/#32aff91e05ba9985a49a76a4fb5338d7

    Downsample the image.

    script example :
     >>> import Image, os, sys
     >>> for filename in sys.argv[1:]:
     >>>     img_resized = resize(file=filename, width=200, height=200)
     >>>     out = file(os.path.splitext(filename)[0]+"_thumb.jpg", "w")
     >>>     try:
     >>>         out.save(img_resized, "JPEG")
     >>>     finally:
     >>>         out.close()

    @param file: an image filename
    @param width: the width of the result image
    @param height: the height of the result image
    @param crop: boolean - crop the image to fill the box
    @param quality: quality of the result image

    @return out: file-like-object - save the image into the output stream
    '''
    img = Image.open(file)
    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0] / factor > 2 * width and img.size[1] * 2 / factor > 2 * height:
        factor *= 2
    if factor > 1:
        img.thumbnail((img.size[0] / factor, img.size[1] / factor),
                      Image.NEAREST)

    #calculate the cropping box and get the cropped part
    if crop:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / width
        hRatio = 1.0 * y2 / height
        if hRatio > wRatio:
            y1 = y2 / 2-height * wRatio / 2
            y2 = y2 / 2 + height * wRatio / 2
        else:
            x1 = x2 / 2-width * hRatio / 2
            x2 = x2 / 2 + width * hRatio / 2
        img = img.crop((x1, y1, x2, y2))

    # Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail((width, height), Image.ANTIALIAS)

    # Save it into a file-like object
    out = StringIO()
    img.save(out, "JPEG", quality=75)

    return out
