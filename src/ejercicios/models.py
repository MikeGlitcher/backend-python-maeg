from django.db import models

# Create your models here.

class ProductModels(models.Model):
    title = models.TextField()
    price = models.FloatField()
    description = models.TextField(null=True)
    color = models.TextField()

    def det_absolute_url(self):
        print(f"/product/{self.name + len(self.name) + self.name[0] + self.name[-1]}")
        return f"/product/{self.name + len(self.name) + self.name[0] + self.name[-1]}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)