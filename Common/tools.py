import base64
from io import StringIO, BytesIO

from django.db import models
from PIL import Image
from django.core.files.base import ContentFile



def convertToFile(data,filename):
    return ContentFile(base64.b64decode(data), name='{}'.format(filename))

def resizeImage(image, image_size=None):
    filename = image.name

    image = Image.open(image)
    if image_size is not None:
        image.thumbnail((image_size, image_size))
    try:
        return getContent(image, filename)
    except:
        return getContent(image, filename[:filename.index(".")] + "." + image.format.lower())



def resizeEncodedImage(image,image_name,image_size=200):
    image=ContentFile(base64.b64decode(image), name='{}'.format(image_name))
    return resizeImage(image,image_size=image_size)

"""
    GETIMAGETYPE, RETURNS THE TYPE OF THE INPUTTED IMAGE, AND THIS SHOULD BE UPDATED
    IN CASE OTHER FORMATS ARE INTRODUCES, AS OF NOW ONLY JPEG AND PNG ARE SUPPORTED
"""


def getImageType(imagename):
    if "PNG" in imagename.upper():
        print("png image detected")
        return "PNG"
    else:
        print("jpeg image detected")
        return "JPEG"


"""
    THIS METHOD IS USED FOR TAKING IN PIL EDITING IMAGE AND CONVERT IT INTO IN MEMORY OBJECT FOR BEING 
    FURTHER PROCESSED AND EASILY SAVED INTO THE IMAGE FIELD IN 

    INPUT : IMAGE ==> PILLOW TYPE, FILENAME==>STRING
    OUTPUT : IMAGE ==> IN MEMORY UPLOAD TYPE
"""


def getContent(image, filename):
    img_io = BytesIO()
    try:
        image.save(img_io, format=getImageType(filename))
    except:
        image = image.convert("RGB")
        image.save(img_io, format="JPEG")
    # image.save(img_io, format=getImageType(filename), quality=100)
    img_content = ContentFile(img_io.getvalue(), filename)
    return img_content


def getExtension(filename):
    if "PNG" in filename.upper():
        return "png"
    elif "PDF" in filename.upper():
        return "pdf"
    elif "JPG" in filename.upper() or "JPEG" in filename.upper():
        return "jpg"





def stripEmojis(text: str):
    return "".join([character for character in text if len(character.encode("utf8")) <= 2])


def stripSymbols(text: str):
    import re
    patter = re.compile("[^\w\d]+")
    return patter.sub(" ", text)