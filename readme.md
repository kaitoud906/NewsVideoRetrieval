# Load/remove embeddings
    python manage.py load_embeddings
    python manage.py remove_embeddings

Chỉnh thông tin file ảnh và embeddings trong `videoretrieval\myapp\management\commands\load_embeddings.py`

Chỉnh folder ảnh được lấy trong `videoretrieval\videoretrieval\settings.py`
<!-- chcp 1252 -->

# Migration
    python manage.py makemigrations
    python manage.py migrate

# Run server
    python manage.py runserver
