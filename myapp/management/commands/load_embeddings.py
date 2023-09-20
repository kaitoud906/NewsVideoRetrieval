import os
import numpy as np
from django.core.management.base import BaseCommand
from myapp.models import ImageEmbedding  # Import your ImageData model
from glob import glob
import json

class Command(BaseCommand):
    help = 'Load image embeddings into the database'

    def handle(self, *args, **options):
        all_keyframe = glob('D:\AI_Challenge\Data\\keyframes\\*\\*.jpg')
        video_keyframe_dict={}
        for kf_path in all_keyframe:
            _, vid, kf = kf_path[:-4].rsplit('\\',2)
            relative_path = kf_path.split('\\',3)[-1]
            if vid not in video_keyframe_dict.keys():
                video_keyframe_dict[vid] = [relative_path]
            else:
                video_keyframe_dict[vid].append(relative_path)

        for k,v in video_keyframe_dict.items():
            video_keyframe_dict[k] = sorted(v)

        all_video = list(video_keyframe_dict.keys())
        for v in all_video:
            clip_path = f'D:\AI_Challenge\Data\clip-features-vit-b32\\{v}.npy'
            a = np.load(clip_path)

            for i,k in enumerate(video_keyframe_dict[v]):
                embedding = json.dumps(a[i].tolist())
                image_data = ImageEmbedding(image_embedding=embedding, image_path=k)
                image_data.save()


        self.stdout.write(self.style.SUCCESS(f'Successfully loaded embeddings.'))
