import uuid, hashlib, time

SESSION_DURATION = 86400

def generate_password_digest(user):
    user.salt = uuid.uuid4().hex
    user.password_digest = hashlib.sha512(password + salt).hexdigest()

def generate_token(user):
    user.token = uuid.uuid4().hex
    user.token_expire_time = _currentTime() + SESSION_DURATION

# @staticmethod
# def token_is_valid(user, token)
#     return (user.token == token) && (user.token_expire_time < _currentTime())

def password_is_valid(user, password):
    input_digest = hashlib.sha512(password + user.salt).hexdigest()
    return user.password_digest == input_digest

def _currentTime():
    return int(time.time())

class Authenticator:
    def __init__(self, model, token):
        self.current_user = model.objects.filter(token=token, token_expire_time__gt=_currentTime()).first()
