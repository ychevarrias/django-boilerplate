from uuid import uuid4
from random import randint
from django.conf import settings
from django.core.cache import cache

TOKEN_SECONDS_LIFE = 60*10
PUBLIC_TOKEN_SENDED = f"public_token_sended"
PUBLIC_TOKEN_KEY = f"public_token_key"


def _set_token_created():
    cache.set(PUBLIC_TOKEN_SENDED, True, TOKEN_SECONDS_LIFE)


def _unset_token_created():
    cache.delete(PUBLIC_TOKEN_SENDED)


def check_sended():
    return cache.get(PUBLIC_TOKEN_SENDED) or False


def get_token(diff=2):
    hashed_string = uuid4().hex
    token = hashed_string[-16:]
    cache.set(PUBLIC_TOKEN_KEY, token, TOKEN_SECONDS_LIFE)
    _set_token_created()
    return token


def validate_token(token, clear=False):
    if not cache.get(PUBLIC_TOKEN_KEY) == token:
        return False
    if clear:
        cache.delete(PUBLIC_TOKEN_KEY)
        _unset_token_created()
    return True


def get_pin():
    pin = str(randint(11111, 999999)).zfill(6)
    cache.set(PUBLIC_TOKEN_KEY, pin, TOKEN_SECONDS_LIFE)
    _set_token_created()
    return pin


def validate_ping(pin, clear=False):
    if not cache.get(pin) == PUBLIC_TOKEN_KEY:
        return False
    if clear:
        cache.delete(PUBLIC_TOKEN_KEY)
        _unset_token_created()
    return True
