# Description
Basic solution for Video Retrieval

# Settings
    pip install -r requirements.txt

Edit image file and embeddings loads in `videoretrieval\myapp\management\commands\load_data.py`

Folder to get image in `videoretrieval\videoretrieval\settings.py`

Video/Image mode: USE_VIDEO trong `videoretrieval\videoretrieval\settings.py`


<!-- chcp 1252 -->
# Data folder structure
```bash
Data
│
├── keyframes
│   ├── L01_V001
│   │   ├── 0001.jpg
│   │   └── ...
│   ├── L01_V002
│   │   ├── 0001.jpg
│   │   ├── ...
│   ├── ...
│ 
├── map-keyframes
│   ├── L01_V001.csv
│   ├── ...
│
├── metadata-b1
│   └── metadata
│       ├── L01_V001.json
│       ├── ...
│
├── clip-features-vit-b32
│   ├── L01_V001.npy
│   ├── ...

```

# Migration

    python manage.py makemigrations
    python manage.py migrate

# Run server
    python manage.py runserver
