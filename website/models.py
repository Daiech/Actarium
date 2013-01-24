from django.db import models


# Create your models here.
class feedBack(models.Model):
    type_feed = models.IntegerField(default=0, max_length=4)
    email = models.CharField(max_length=60, null=False)
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
