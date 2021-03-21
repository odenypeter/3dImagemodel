from django.db import models


class GeneratedFile(models.Model):
    file_name = models.CharField(null=True, blank=True, max_length=250)
    file = models.FileField(upload_to='final_models', null=True, blank=True)

    def __str__(self):
        return f'{self.file_name or self. id}'


class Image(models.Model):
    generated_file = models.ForeignKey(GeneratedFile, related_name='model_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.generated_file or self.id}'
