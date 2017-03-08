# Users

## `POST users/sign_in`
### Request
Body
```
{
    "username": "user01@mail.com",
    "password": "password"
}
```

### Response

#### 200
```
{
    "token": "34611da09e1f4f0195d2591cdda624d4",
    "token_expire_time": 1488856413
}
```
#### 401

----
# Channels
## `GET channels`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
### Response
#### 200
```
[
    {
        "id": 1,
        "name": "March"
    }
]
```
----

# Events

## `GET events`

### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
params
```
?from=1488850000&
to=1488860000&
channel_id=1&
ts=1488850000&
page=1&
per=20
```

### Response
#### 200
```
{
    "total": 101020,
    "page": 1,
    "per": 20,
    "events": [
        {
            "id": 1,
            "title": "Science March",
            "description": "Science doesn't care what you believe.",
            "start_time": 1488850010,
            "end_time": 1488850020,
            "channel_id": 1,
            "channel_name": "March",
            "total_comments": 10,
            "total_likes": 10,
            "total_participants": 10,
            "location": "White House",
            "address": "Washington DC",
            "lat": 100.1234,
            "lon": 100.1234,
            "main_picture": "http://social_events/00001.png",
            "user_like_id": 1,
            "user_participant_id": 1
        }
    ]
}
```
#### 401

## `GET events/10`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```

### Response
#### 200
```
{
    "id": 1,
    "title": "Science March",
    "description": "Science doesn't care what you believe.",
    "start_time": 1488850010,
    "end_time": 1488850020,
    "channel_id": 1,
    "channel_name": "March",
    "total_comments": 10,
    "total_likes": 10,
    "total_participants": 10,
    "location": "White House",
    "address": "Washington DC",
    "lat": 100.1234,
    "lon": 100.1234,
    "main_picture": "http://social_events/images/00001.png",
    "comments": [
        {
            "id": 1,
            "content": "This is awesome!",
            "user_id": 1,
            "reply_comment_id": null,
            "user_full_name": "James Bond",
            "user_portrait": null,
            "create_time": 1488850020
        }
    ],
    "likes": [
        {
            "id": 1,
            "user_id": 2,
            "user_full_name": "Martin Hodges",
            "user_portrait": "http://social_events/images/00001.png",
            "create_time": 1488850020
        }
    ],
    "participants": [
        {
            "id": 1,
            "user_id": 2,
            "user_full_name": "Martin Hodges",
            "user_portrait": "http://social_events/images/00001.png",
            "create_time": 1488850020
        }
    ]
}
```
#### 401
#### 404

----

# Comments

## `GET comments?event_id=1`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
### Response
#### 200
```
[
    {
        "id": 2,
        "content": "Not that interesting...",
        "user_id": 1,
        "user_full_name": "James Bond",
        "user_portrait": "http://social_events/images/0001.png",
        "reply_comment_id": 1,
        "create_time": 1488850020
    }
]
```
#### 401
#### 404

## `POST comments`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
body
```
{
    "content": "Not that interesting...",
    "event_id": 1,
    "user_id": 1,
    "reply_comment_id": 1
}
```

### Response
#### 200
```
{
    "id": 2,
    "content": "Not that interesting...",
    "user_id": 1,
    "reply_comment_id": 1,
    "create_time": 1488850020
}
```
#### 401
#### 404

----

# Likes

## `GET likes?event_id=1`

### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
### Response
#### 200
```
[
    {
        "id": 1,
        "user_id": 2,
        "user_full_name": "Martin Hodges",
        "user_portrait": "http://social_events/images/00001.png",
        "create_time": 1488850020
    }
]
```
#### 401
#### 404

## `POST likes`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
body
```
{
    "event_id": 1
}
```

### Response
#### 200
```
{
    "id": 1,
    "user_id": 2,
    "event_id": 1,
    "create_time": 1488850020
}
```
#### 401
#### 404

## `DELETE likes/1`, `POST unlikes/1`
### Response
#### 200
```
{
    "id": 1,
    "user_id": 2,
    "event_id": 1,
    "create_time": 1488850020,
    "delete_time": 1488850030
}
```
#### 401
#### 404

----

# Participants

## `GET participants?event_id=1`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
### Response
#### 200
```
[
    {
        "id": 1,
        "user_id": 2,
        "user_full_name": "Martin Hodges",
        "user_portrait": "http://social_events/images/00001.png",
        "create_time": 1488850020
    }
]
```
#### 401
#### 404

## `POST participants`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```
body
```
{
    "event_id": 1
}
```
### Response
#### 200
```
{
    "id": 1,
    "user_id": 2,
    "event_id": 1,
    "create_time": 1488850020
}
```
#### 401
#### 404

## `DELETE participants/1`, `POST unparticipants/1`
### Request
header
```
HTTP AUTHORIZATION: Token 34611da09e1f4f0195d2591cdda624d4
```

### Response
#### 200
```
{
    "id": 1,
    "user_id": 2,
    "event_id": 1,
    "create_time": 1488850020,
    "delete_time": 1488850030
}
```
#### 401
#### 404
