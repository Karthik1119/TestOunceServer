from django.db import models
from CustomAuth.models import User
from .constants import AssetConstants
from .tools import resizeImage, resizeEncodedImage, convertToFile


def getImageLocation(instance, filename):
    return "{}/{}".format(instance.user.id if instance.user else "general" , filename)

class Asset(models.Model):
    """
        This class is used to provide support for different file sizes and types:
        for images:
            -->every file type will be used with the appropriate dimension images
        for videos / documents:
            --> only the file type will be used, since it cannot be compressed
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="assets")
    file = models.FileField(upload_to=getImageLocation)
    file_xxl = models.FileField(upload_to=getImageLocation, default=None, null=True, blank=True)  # 1080p
    file_xl = models.FileField(upload_to=getImageLocation, default=None, null=True, blank=True)  # 720p
    file_l = models.FileField(upload_to=getImageLocation, default=None, null=True, blank=True)  # 480p
    icon = models.FileField(upload_to=getImageLocation, default=None, null=True, blank=True)  # 200 dp
    status = models.PositiveSmallIntegerField(choices=AssetConstants.STATUSES,default=AssetConstants.NOT_UPLOADED)
    type = models.PositiveSmallIntegerField(choices=AssetConstants.FILE_TYPES)



    @staticmethod
    def uploadEncodedFile(self,user,file,filename):
        """
        :param file: The encoded file available
        :param filename: The name of the encoded file
        :return: asset object with the saved locations
        """
        asset = None
        if AssetConstants.getFileType(filename) == AssetConstants.IMAGE:
            asset= Asset(
                user=user,
                type = AssetConstants.IMAGE,
                status = AssetConstants.UPLOADED,
                file = resizeEncodedImage(file,filename, image_size= 2000),
                file_xxl = resizeEncodedImage(file,filename, image_size= 1080),
                file_xl=resizeEncodedImage(file,filename, image_size= 720),
                file_l = resizeEncodedImage(file,filename, image_size= 480),
                icon = resizeEncodedImage(file,filename, image_size= 200)
            )
            asset.save()
            return asset
        else:
            asset = Asset(
                user=user,
                type=AssetConstants.DOCUMENT,
                status = AssetConstants.UPLOADED,
                file = convertToFile(file,filename)
            )
            asset.save()
            return asset


    @staticmethod
    def uploadFile(user,file):
        """
        :param user: The user model, which is mainly used for creating the folder name where the files are going to be stored
        :param file: The file available from request.FILES
        :return: asset object with the saved locations
        """
        asset = None
        if AssetConstants.getFileType(file.name) == AssetConstants.IMAGE:
            asset = Asset(
                user=user,
                type=AssetConstants.IMAGE,
                status=AssetConstants.UPLOADED,
                file=resizeImage(file, image_size=2000),
                file_xxl=resizeImage(file, image_size=1080),
                file_xl=resizeImage(file, image_size=720),
                file_l=resizeImage(file, image_size=480),
                icon=resizeImage(file, image_size=200)
            )
            asset.save()
            return asset
        else:
            asset = Asset(
                user=user,
                type=AssetConstants.DOCUMENT,
                status=AssetConstants.UPLOADED,
                file=file
            )
            asset.save()
            return asset
