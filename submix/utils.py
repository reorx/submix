import base64


def base64_encode_str(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def base64_decode_str(s: str) -> str:
    return base64.b64decode(s.encode()).decode()


def setup_django():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'submix.settings')
    import django
    django.setup()
