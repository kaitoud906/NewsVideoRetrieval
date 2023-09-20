from django.db import models
from django.contrib.postgres.fields import ArrayField
import json
import numpy as np

class ImageEmbedding(models.Model):
    image_path  = models.FileField(upload_to='images/')
    image_embedding = models.TextField()

    def get_image_embedding(self):
        return np.array(json.loads(self.image_embedding))

    def __str__(self):
        return self.image_path.name