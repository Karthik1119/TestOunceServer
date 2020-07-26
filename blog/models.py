from django.db import models

# Create your models here.
from Common.models import Asset
from CustomAuth.model.user import User
from .constants import BlogConstants


class Category(models.Model):
    # ai, android, ios
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey(Asset,on_delete=models.CASCADE,null=True,default=None,related_name="categories")
    title = models.CharField(max_length=100,blank=True,default=None,null=True)
    followers = models.ManyToManyField(through="CategoryFollowers.user",related_name="categories_following")


class Blog(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150,blank=True,default=None,null=True)
    description = models.TextField(default=None,null=True,blank=True)
    images = models.ManyToManyField(Asset,on_delete=models.CASCADE,related_name="blogs")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,default=None,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="liked_blogs")
    visibility = models.PositiveSmallIntegerField(choices=BlogConstants.VISIBILITY,default=BlogConstants.VISIBILE)



class CategoryFollowers(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


