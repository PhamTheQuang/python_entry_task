import uuid, hashlib, time

from django.core.cache import cache

SESSION_DURATION = 86400

def generate_password_digest(user):
    user.salt = uuid.uuid4().hex
    user.password_digest = hashlib.sha512(user.password + user.salt).hexdigest()

def generate_token(user):
    if user.token:
        key = _token_cache_key(user.token)
        cache.delete(key)
    user.token = uuid.uuid4().hex
    user.token_expire_time = _current_time() + SESSION_DURATION

def password_is_valid(user, password):
    input_digest = hashlib.sha512(password + user.salt).hexdigest()
    return user.password_digest == input_digest

def sign_in(model, username, password):
    user = model.objects.filter(username=username).first()
    if user and password_is_valid(user, password):
        generate_token(user)
        user.save()
        return user

def get_user(model, token):
    key = _token_cache_key(token)
    user = cache.get(key)
    if not user:
        user = model.objects.filter(token=token, token_expire_time__gt=_current_time()).first()
        if user:
            cache.set(key, user)
    return user

def _current_time():
    return int(time.time())

def _token_cache_key(token):
    return 'users.with_token.' + token
