import os
import numpy as np
from django.core.management.base import BaseCommand
from myapp.models import DataStorage,CLIPEmbedding
from glob import glob
import json
import faiss
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer


class Command(BaseCommand):
    help = 'Load data'

    def handle(self, *args, **options):

        # load embeddings
        all_keyframe = glob('D:\AI_Challenge\Data\\keyframes\\*\\*.jpg')

        embeddings = []
        all_path = []

        video_keyframe_dict={}
        for kf_path in all_keyframe:
            _, vid, kf = kf_path[:-4].rsplit('\\',2)
            relative_path = kf_path.split('\\',3)[-1]
            if vid not in video_keyframe_dict.keys():
                video_keyframe_dict[vid] = [relative_path]
            else:
                video_keyframe_dict[vid].append(relative_path)
            all_path.append(relative_path)

        for k,v in video_keyframe_dict.items():
            video_keyframe_dict[k] = sorted(v)

        all_video = list(video_keyframe_dict.keys())
        for v in all_video:
            clip_path = f'D:\AI_Challenge\Data\clip-features-vit-b32\\{v}.npy'
            a = np.load(clip_path)

            for i,k in enumerate(video_keyframe_dict[v]):
                embeddings.append(np.array(a[i]).astype('float32'))

        embeddings = np.array(embeddings)
        all_path = np.array(all_path)
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        DataStorage.index = index
        DataStorage.all_path = all_path

        # load model

        device = "cpu"
        # Define the model ID
        model_ID = "openai/clip-vit-base-patch32"
        # Get model, processor & tokenizer
        
        CLIPEmbedding.model = CLIPModel.from_pretrained(model_ID).to(device)
 	    # Get the processor
        # CLIPModel.processor = CLIPProcessor.from_pretrained(model_ID)
        # Get the tokenizer
        CLIPEmbedding.tokenizer = CLIPTokenizer.from_pretrained(model_ID)
        # Return model, processor & tokenizer


        self.stdout.write(self.style.SUCCESS(f'Successfully loaded data.'))
