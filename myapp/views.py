from django.shortcuts import render
from .models import ImageEmbedding
# from django.http import HttpResponseRedirect
# from .forms import ImageUploadForm
# from django.conf import settings
# from django.db.models import F
# from scipy.spatial.distance import cosine
# from django.http import JsonResponse

import numpy as np
import json
import torch
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer
from sklearn.metrics.pairwise import cosine_similarity

# from django.core.paginator import Paginator

from django.db.models import Func

class GetImageEmbedding(Func):
    function = 'get_image_embedding'

def get_model_info(model_ID, device):
    # Save the model to device
	model = CLIPModel.from_pretrained(model_ID).to(device)
 	# Get the processor
	processor = CLIPProcessor.from_pretrained(model_ID)
    # Get the tokenizer
	tokenizer = CLIPTokenizer.from_pretrained(model_ID)
       # Return model, processor & tokenizer
	return model, processor, tokenizer
# Set the device
# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
# Define the model ID
model_ID = "openai/clip-vit-base-patch32"
# Get model, processor & tokenizer
model, processor, tokenizer = get_model_info(model_ID, device)

def index(request):
    return render(request, 'myapp/index.html')

def display_images(request):
    # Get a list of image filenames in the 'media' directory
    images = ImageEmbedding.objects.all()
    images = images[:100]

    image_urls = []
    for e in images:
        node = {
          "url": e.image_path.url,
          "frame_id": e.image_path.url.split("/")[-1].split(".")[0],
          "video": e.image_path.url.split("/")[-2]
        }
        image_urls.append(node)

    # paginator = Paginator(image_urls,per_page=25)
    # page_number =  request.GET.get('page')
    # page = paginator.get_page(page_number)
    # data = {
    #     'html': render(request, 'myapp/index.html', {'image_urls': image_urls}),
    #     'has_more': page.has_next(),
    # }
    # return JsonResponse(data)

    return render(request, 'myapp/index.html', {'image_urls': image_urls})

def get_single_text_embedding(text):
    inputs = tokenizer(text, return_tensors = "pt")
    text_embeddings = model.get_text_features(**inputs)
    # convert the embeddings to numpy array
    embedding_as_np = text_embeddings.cpu().detach().numpy()
    return embedding_as_np

def get_image_embedding(image_retrieve):
    return np.array(json.loads(image_retrieve))

def similarity(request):
    if request.method == 'POST':
        # Get the query text entered by the user
        query_text = request.POST.get('query')

    query_embedding = get_single_text_embedding(query_text).squeeze(0)
    image_items = np.array(ImageEmbedding.objects.all())
    image_embeddings = [item.get_image_embedding() for item in ImageEmbedding.objects.all()]

    similarities = cosine_similarity([query_embedding], image_embeddings)[0]
    sorted_indices = np.argsort(similarities)[::-1]
    image_items = image_items[sorted_indices].tolist()

    # Extract image URLs
    top_k_images = image_items[:200]

    image_urls = []
    for e in top_k_images:
        node = {
          "url": e.image_path.url,
          "frame_id": e.image_path.url.split("/")[-1].split(".")[0],
          "video": e.image_path.url.split("/")[0]
        }
        image_urls.append(node)
    
    return render(request, 'myapp/index.html', {'image_urls': image_urls})
