from django.db import models
from django.contrib.postgres.fields import ArrayField
import json
import numpy as np
import faiss

# class EmbeddingManager(models.Manager):
#     def create_index(self):
#         embeddings = self.all().values_list('image_embedding', flat=True)
#         embeddings = [np.array(json.loads(embedding)).astype('float32') for embedding in embeddings]
#         # print(embeddings[:5])
#         embeddings = np.array(embeddings)
#         index = faiss.IndexFlatIP(embeddings.shape[1])  # Assuming fixed dimension

#         index.add(embeddings)

#         return index
    
#     def search_similar_embeddings(self, query_vector, k=10):
#         index = self.create_index()
#         distances, indices = index.search(np.array([query_vector], dtype=np.float32), k)

#         results = []
#         for dist, idx in zip(distances[0], indices[0]):
#             # Retrieve the corresponding database object by index
#             obj = self.get(pk=idx + 1)  # Adjust for 0-based vs. 1-based indexing
#             results.append(obj)

#         return results

# class ImageEmbedding(models.Model):
#     image_path  = models.FileField(upload_to='images/')
#     # image_embedding = models.BinaryField()
#     objects = EmbeddingManager()
#     image_embedding = models.TextField()

#     def __str__(self):
#         return self.image_path.name

class DataStorage:
    index = None
    all_path = None

class CLIPEmbedding:
    model = None
    processor = None
    tokenizer = None