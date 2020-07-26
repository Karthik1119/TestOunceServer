

class AssetConstants:
    VIDEO=0;IMAGE=1;DOCUMENT=2
    FILE_TYPES=((IMAGE,"Image"),(VIDEO,"Video"),(DOCUMENT,"Document"))

    NOT_UPLOADED=1;UPLOADED=2;DELETED=3;
    STATUSES = ((NOT_UPLOADED,"Not Uploaded"),(UPLOADED,"Uploaded"),(DELETED,"Deleted"))


    @staticmethod
    def getFileType(filename):
        name=filename.upper()
        if name in ['JPG',"JPEG","PNG"]:
            return AssetConstants.IMAGE
        elif name in ['MPG',"MPEG","FLV"]:
            return AssetConstants.VIDEO
        else:
            return AssetConstants.DOCUMENT
