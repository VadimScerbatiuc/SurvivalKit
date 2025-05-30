import os
from django.conf import settings


def get_image_paths(folder_name):
    folder = os.path.join(settings.MEDIA_ROOT, folder_name)
    images = []
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                images.append(f"{settings.MEDIA_URL}{folder_name}/{filename}")
    return images