# Install package
    pip install -r requirements.txt

Chỉnh thông tin file ảnh và embeddings trong `videoretrieval\myapp\management\commands\load_data.py`

Chỉnh folder ảnh được lấy trong `videoretrieval\videoretrieval\settings.py`
<!-- chcp 1252 -->

# Migration
    python manage.py makemigrations
    python manage.py migrate

# Run server
    python manage.py runserver
