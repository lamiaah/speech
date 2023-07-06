from django.db import models




# Create your models here.
class Convert(models.Model):
    id  = models.AutoField(null=False,blank=False,primary_key=True)
    uploaded_file =models.FileField(upload_to="audio_file",null=True, blank=False)
    # uploaded_file =models.PositiveBigIntegerField(null=True, blank=False)
    # uploaded_file =models.BinaryField(null=True, blank=False)
    exported_file = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.uploaded_file
