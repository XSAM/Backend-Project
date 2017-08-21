from flask import session
from flask_socketio import emit, join_room, leave_room
from routes import current_user

# attention: multi import
from app import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    u = current_user()
    room = message.get('room')
    join_room(room)
    emit('status', {'msg': u.username + ' 进入房间'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    u = current_user()
    room = message.get('room')
    emit('message', {'msg': u.username + ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    u = current_user()
    room = message.get('room')
    leave_room(room)
    emit('status', {'msg': u.username + ' 离开房间'}, room=room)

