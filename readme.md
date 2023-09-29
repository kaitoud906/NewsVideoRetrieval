# Settings
    pip install -r requirements.txt

Chỉnh thông tin file ảnh và embeddings trong `videoretrieval\myapp\management\commands\load_data.py`

Chỉnh folder ảnh được lấy trong `videoretrieval\videoretrieval\settings.py`

Chỉnh chế độ xem video hay xem ảnh: USE_VIDEO trong `videoretrieval\videoretrieval\settings.py`


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
Không cần sử dụng

    python manage.py makemigrations
    python manage.py migrate

# Run server
    python manage.py runserver
