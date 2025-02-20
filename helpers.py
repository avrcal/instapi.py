import os
from instagrapi.exceptions import ClientError
from ..models import Media, User

class HelperFunctions:
    @staticmethod
    def validate_media_path(path: str, max_size: int) -> bool:
        if not os.path.exists(path):
            return False
        if os.path.getsize(path) > max_size:
            return False
        return True

    @staticmethod
    def media_to_model(media: dict) -> Media:
        return Media(
            pk=media['pk'],
            caption=media.get('caption', ''),
            media_type=media['media_type'],
            user=User(media['user'])
        )

    @staticmethod
    def handle_api_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientError as e:
                print(f"[API ERROR] {str(e)}")
                return None
        return wrapper

    @staticmethod
    def format_caption(base_caption: str, **kwargs) -> str:
        return base_caption.format(**kwargs)