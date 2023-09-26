from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from .forms import ImageUploadForm
# from django.conf import settings
# from django.db.models import F
# from scipy.spatial.distance import cosine
# from django.http import JsonResponse

import numpy as np
import json
import torch
import pandas as pd
from videoretrieval.settings import MEDIA_URL, USE_VIDEO
# import faiss

from myapp.models import DataStorage, CLIPEmbedding

# from django.core.paginator import Paginator

def index(request):
    return render(request, 'myapp/index.html')

def display_images(request):
    # Get a list of image filenames in the 'media' directory
    k = 100
    if request.method == 'POST':
        # Get the query text entered by the user
        k = int(request.POST.get('k'))
    images = DataStorage.all_path[:k]

    image_urls = []
    for e in images:
        node = {
          "url": MEDIA_URL + e.replace('\\', '/'),
          "frame_id": e.split("\\")[-1].split(".")[0],
          "video": e.split("\\")[1]
        }
        image_urls.append(node)

    return render(request, 'myapp/index.html', {'image_urls': image_urls,'use_video': USE_VIDEO})

def get_single_text_embedding(text):
    inputs = CLIPEmbedding.tokenizer(text, return_tensors = "pt")
    text_embeddings = CLIPEmbedding.model.get_text_features(**inputs)
    # convert the embeddings to numpy array
    embedding_as_np = text_embeddings.cpu().detach().numpy()
    return embedding_as_np

def similarity(request):
    k = 100
    if request.method == 'POST':
        # Get the query text entered by the user
        query_text = request.POST.get('query')
        k = int(request.POST.get('k'))
        if query_text == '':
            return display_images(request)
    # show_video = True

    query_embedding = get_single_text_embedding(query_text).astype('float32')

    distances, indices = DataStorage.index.search(query_embedding, k)

    top_k_images = DataStorage.all_path[indices].squeeze(0).tolist()
    # top_k_images.reverse()
    
    # Extract image URLs

    image_urls = []
    for e in top_k_images:
        node = {
          "url": MEDIA_URL + e.replace('\\', '/'),
          "frame_id": e.split("\\")[-1].split(".")[0],
          "video": e.split("\\")[1]
        }
        image_urls.append(node)
    
    return render(request, 'myapp/index.html', {'image_urls': image_urls, 'old_query':query_text, "use_video": USE_VIDEO})
