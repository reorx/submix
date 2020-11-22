import base64
import binascii
import dataclasses

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


def base64_encode_str(s: str, urlsafe=False) -> str:
    if urlsafe:
        return base64.urlsafe_b64encode(s.encode()).decode()
    else:
        return base64.b64encode(s.encode()).decode()


def base64_decode_str(s: str, urlsafe=True) -> str:
    # To avoid `incorrect padding` error, ref: https://stackoverflow.com/a/2942039/596206
    s += '=' * (-len(s) % 4)
    try:
        if urlsafe:
            return base64.urlsafe_b64decode(s.encode()).decode()
        else:
            return base64.b64decode(s.encode()).decode()
    except binascii.Error:
        print(f'base64.b64decode: {s}')
        raise


def base64_decode_bytes(s: bytes, urlsafe=True) -> bytes:
    s += b'=' * (-len(s) % 4)
    try:
        if urlsafe:
            return base64.urlsafe_b64decode(s)
        else:
            return base64.b64decode(s)
    except binascii.Error:
        print(f'base64.b64decode: {s}')
        raise


def get_base64_config_from_url(url, scheme) -> str:
    """get config str for base64 url like vmess:// or ssr://"""
    return base64_decode_str(url[len(scheme) + 3:])


def setup_django():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'submix.settings')
    import django
    django.setup()


def api_data(o):
    return {'data': o}


def json_response(data, status=200, encoder=None, json_dumps_params=None, **kwargs):
    json_dumps_params = json_dumps_params or {}
    json_dumps_params.update({'ensure_ascii': False})

    return JsonResponse(
        data,
        encoder=encoder or DataclassJSONEncoder,
        json_dumps_params=json_dumps_params,
        safe=False,
        status=status,
        **kwargs,
    )


class DataclassJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def make_json_encoder_for_type(type_class, func):
    class CustomEncoder(DataclassJSONEncoder):
        def default(self, o):
            if isinstance(o, type_class):
                return func(o)
            return super(CustomEncoder, self).default(o)

    return CustomEncoder
