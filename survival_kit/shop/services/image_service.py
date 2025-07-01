import os
from django.conf import settings


def get_image_paths(directory_name: str) -> list:
    image_paths = []
    directory_path = os.path.join(settings.MEDIA_ROOT, directory_name)
    if not os.path.exists(directory_path):
        return image_paths

    for file_name in os.listdir(directory_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
            image_paths.append(os.path.join(settings.MEDIA_URL, directory_name, file_name))

    return image_paths