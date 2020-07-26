from django.db import models

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    device_id = models.CharField(max_length=200, default=None, null=True, blank=True)
    version_id = models.CharField(max_length=200,default=None,null=True,blank=True)

    class Meta:
        unique_together = (('device_id','name'),)