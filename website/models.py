from django.db import models


# Create your models here.
class feedBack(models.Model):
    type_feed = models.IntegerField(default=0, max_length=4)
    email = models.CharField(max_length=60, null=False)
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "[%s] %s: %s " % (self.type_feed, self.email, self.comment)


class faq(models.Model):
    question = models.CharField(max_length=150, verbose_name="Pregunta")
    answer = models.TextField(max_length=60, null=False, verbose_name="Respuesta")
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now=True)
