
# If store in local server
def public_url(key):
    if key:
        return key.url
    else:
        return ""
