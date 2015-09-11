from django.db import models

from django.contrib.auth.models import User,  Group
# Create your models here.



class MV_Template(models.Model):
    mv_name = models.CharField(max_length = 255, blank = True, null = True)
    mv_file_location = models.FileField(upload_to="mv_templates", max_length=255)


    def __unicode__(self):
        return u'%s' \
                % (self.mv_name)


class Subtitle_Template(models.Model):
    subtitle_name = models.CharField(max_length = 255, blank = True, null = True)
    subtitle_file_location = models.FileField(upload_to="subtitle_templates", max_length=255)


    def __unicode__(self):
        return u'%s' \
                % (self.subtitle_name)

class Music(models.Model):
    music_name = models.CharField(max_length = 255, blank = True, null = True)
    music_mv = models.ForeignKey(MV_Template)
    music_subtitle = models.ForeignKey(Subtitle_Template)

    def __unicode__(self):
        return u'%s' \
                % (self.music_name)

