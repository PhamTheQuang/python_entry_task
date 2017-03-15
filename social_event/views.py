import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.utils.decorators import decorator_from_middleware
from django.forms.util import ValidationError
from django.core.cache import cache

from social_event.services import authentication, attachment
from social_event.models import *
from social_event.middlewares import *

MAX_RESULT_PER_PAGE = 10

@require_POST
@csrf_exempt
def user_sign_in(request):
    user = authentication.sign_in(User, request.POST.get("username"), request.POST.get("password"))
    if user:
        resp = {"token": user.token, "token_expire_time": user.token_expire_time}
        return _json_response(resp)
    else:
        return _json_error_response(401, "Unauthorized")

@require_GET
@decorator_from_middleware(TokenValidateMiddleware)
def channels(request):
    resp = map(lambda channel: {"id": channel.id, "name": channel.name}, Channel.objects.all())
    return _json_response(resp)

@require_GET
@decorator_from_middleware(TokenValidateMiddleware)
def event(request, id):
    key = "event.with_id" + str(id)
    resp = cache.get(key)
    if not resp:
        event = get_object_or_404(Event, id=id)
        resp = _render_event(event)
        cache.set(key, resp)
    return _json_response(resp)

@require_GET
@decorator_from_middleware(TokenValidateMiddleware)
def events(request):
    timestamp = request.GET.get('ts')
    if not timestamp:
        return _json_error_response(403, "Timestamp required")

    try:
        channel_id = request.GET.get('channel_id')
        from_time = request.GET.get('from')
        to_time = request.GET.get('to')
        page = int(request.GET.get('page') or 1)
        per = int(request.GET.get('per') or MAX_RESULT_PER_PAGE)
        offset = (page - 1) * per

        key = _events_cache_key(channel_id, from_time, to_time, page, per)
        resp = cache.get(key)

        if not resp:
            events = Event.objects.filter(create_time__lte=timestamp)
            if channel_id:
                events = events.filter(channel_id=channel_id)
            if from_time:
                events = events.filter(end_time__gt=from_time)
            if to_time:
                events = events.filter(start_time__lt=to_time)

            total = events.count()
            # TODO: Check if should add index here
            events = events.order_by('start_time', 'end_time').all()[offset:offset+per]
            event_list = list(events) # eager load events
            user_likes = _to_dict(Like.objects.filter(user=request.current_user, event__in=event_list), 'event_id')
            user_participants = _to_dict(Participant.objects.filter(user=request.current_user, event__in=event_list), 'event_id')
            resp = {
                "total": total,
                "page": page,
                "per": per,
                "events": _render_events(event_list, user_likes, user_participants)
            }
            cache.set(key, resp)

        return _json_response(resp)
    except ValueError:
        return _json_error_response(400, "Incorrect data format")

@csrf_exempt
@require_http_methods(["GET", "POST"])
@decorator_from_middleware(TokenValidateMiddleware)
@decorator_from_middleware(RequireEventMiddleware)
def comments(request):
    if request.method == "POST":
        try:
            comment = request.event.create_comment(content=request.POST.get('content'), user=request.current_user)
        except ValidationError as e:
            return _json_error_response(400, e.message_dict)
        resp = _render_attributes_of(comment, "id", "content", "user_id", "reply_comment_id", "event_id", "create_time")
        return _json_response(resp)
    else:
        key = "comments.with_event_id." + str(request.event.id)
        resp = cache.get(key)
        if not resp:
            comments = Comment.objects.filter(event=request.event)
            resp = _render_comments(comments)
            cache.set(key, resp)
        return _json_response(resp)

@csrf_exempt
@require_POST
@decorator_from_middleware(TokenValidateMiddleware)
def unlike(request, id):
    like = get_object_or_404(Like, id=id, user=request.current_user)
    like.event.delete_like(like)
    resp = _render_attributes_of(like, "id", "user_id", "event_id", "create_time")
    resp["delete_time"] = int(time.time())
    return _json_response(resp)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@decorator_from_middleware(TokenValidateMiddleware)
@decorator_from_middleware(RequireEventMiddleware)
def likes(request):
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        try:
            like = request.event.create_like(user=request.current_user)
        except ValidationError as e:
            return _json_error_response(400, e.message_dict)
        resp = _render_attributes_of(like, "id", "user_id", "event_id", "create_time")
        return _json_response(resp)
    else:
        key = "likes.with_event_id." + str(request.event)
        resp = cache.get(key)
        if not key:
            likes = request.event.like_set.all()
            resp = _render_interactions(likes)
            cache.set(key, resp)
        return _json_response(resp)

@csrf_exempt
@require_POST
@decorator_from_middleware(TokenValidateMiddleware)
def unparticipate(request, id):
    participant = get_object_or_404(Participant, id=id, user=request.current_user)
    participant.event.delete_participant(participant)
    resp = _render_attributes_of(participant, "id", "user_id", "event_id", "create_time")
    resp["delete_time"] = int(time.time())
    return _json_response(resp)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@decorator_from_middleware(TokenValidateMiddleware)
@decorator_from_middleware(RequireEventMiddleware)
def participants(request):
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        try:
            participant = request.event.create_participant(user=request.current_user)
        except ValidationError as e:
            return _json_error_response(400, e.message_dict)
        resp = _render_attributes_of(participant, "id", "user_id", "event_id", "create_time")
        return _json_response(resp)
    else:
        key = "participants.with_event_id." + str(request.event)
        resp = cache.get(key)
        if not key:
            participants = request.event.participant_set.all()
            resp = _render_interactions(participants)
            cache.set(key, resp)
        return _json_response(resp)

# TODO: Move this to utilities
def _to_dict(list, attribute):
    res = {}
    for item in list:
        res[getattr(item, attribute)] = item
    return res

def _json_response(body, status=200):
    return HttpResponse(json.dumps(body), status=status, content_type="application/json")

def _json_error_response(status, *errors):
    return _json_response({"errors": errors}, status)

def _events_cache_key(channel_id, from_time, to_time, page, per):
    return "events.search.{0}.{1}.{2}.{3}.{4}".format(channel_id, from_time, to_time, page, per)

#============= RENDER METHODS =======================
# Similar to template, but construct dict object here

def _render_events(events, user_likes, user_participants):
    res = []
    for event in events:
        event_res = _render_attributes_of(event, "id", "title", "description", "start_time", "end_time", "channel_id", "total_comments", "total_likes", "total_participants", "location", "address", "lat", "lon")
        event_res["main_picture"] = attachment.public_url(event.main_picture)

        user_like = user_likes.get(event.id)
        event_res["user_like_id"] = user_like.id if user_like else None

        user_participant = user_participants.get(event.id)
        event_res["user_participant_id"] = user_participant.id if user_participant else None

        res.append(event_res)
    return res

def _render_event(event):
    res = _render_attributes_of(event, "id", "title", "description", "start_time", "end_time", "channel_id", "total_comments", "total_likes", "total_participants", "location", "address", "lat", "lon")
    res['channel_name'] = event.channel.name
    res['main_picture'] = attachment.public_url(event.main_picture)
    # res['pictures'] = _render_pictures(event.picture_set)
    res['comments'] =_render_comments(event.comment_set.all())
    res['likes'] = _render_interactions(event.like_set.all())
    res['participants'] = _render_interactions(event.participant_set.all())
    return dict(res)

def _render_pictures(pictures):
    return map(attachment.public_url, pictures)

def _render_comments(comments):
    return map(_render_comment, comments.prefetch_related('user'))

def _render_comment(comment):
    res = _render_attributes_of(comment, "id", "content", "user_id", "create_time", "reply_comment_id")
    res["user_full_name"] = comment.user.full_name
    res["user_portrait"] = attachment.public_url(comment.user.portrait)
    return res

def _render_interactions(interactions):
    return map(_render_interaction, interactions.prefetch_related('user'))

def _render_interaction(interaction):
    res = _render_attributes_of(interaction, "id", "user_id", "create_time")
    res["user_full_name"] = interaction.user.full_name
    res["user_portrait"] = attachment.public_url(interaction.user.portrait)
    return res

def _render_attributes_of(obj, *args):
    res = {}
    for arg in args:
        res[arg] = getattr(obj, arg)
    return res
