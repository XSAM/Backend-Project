from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    session,
    abort,
)
from utils import log
from models.todo import Todo

from routes import (
    current_user,
    validate_login_and_token_with_json,
    validate_login_and_token_with_form,
    csrf_token,
    get_valid_with_form,
)
import uuid

main = Blueprint('api_todo', __name__)


@main.route('/<int:todo_id>', methods=['PATCH', 'DELETE'])
def delete(todo_id):
    code, u = validate_login_and_token_with_json(request)
    t = Todo.find_one(id=todo_id)
    if code == 200:
        if request.method == 'PATCH':
            form = request.get_json()
            if t is not None and t.user_id == u.id:
                new_title = form.get('title', '')
                log('User: {},Edit todo,before Title: {}, after Title: {}'.format(u.id, t.title, new_title))
                t.update({
                    'title': new_title,
                })
                return 'success'
        elif request.method == 'DELETE':
            if t.user_id == u.id:
                log('User: {},Delete todo,Title: {},'.format(u.id, t.title))
                t.delete()
                return 'success'

    abort(code)


@main.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    code, u = validate_login_and_token_with_json(request)
    form = request.get_json()
    if code == 200:
        t = Todo.find_one(id=todo_id)
        if t is not None and t.user_id == u.id:
            log('User: {},Completed todo,Title: {},'.format(u.id, t.title))
            complete = form.get('complete', False)
            Todo.complete(t.id, complete)
            return 'success'
        else:
            abort(403)
    else:
        abort(code)


@main.route('/', methods=['POST'])
def add():
    code, u = validate_login_and_token_with_json(request)
    form = request.get_json()
    if code == 200:
        title = form.get('title', '')
        log('User: {},Add todo,Title: {}'.format(u.id, title))
        Todo().new({
            'user_id': u.id,
            'title': title,
        })
        return 'success'
    else:
        abort(code)


# deprecated
@main.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    code, u = validate_login_and_token_with_json(request)
    form = request.get_json()
    if code == 200:
        t = Todo.find_one(id=todo_id)
        if t is not None and t.user_id == u.id:
            new_title = form.get('title', '')
            log('User: {},Edit todo,before Title: {}, after Title: {}'.format(u.id, t.title, new_title))
            t.update({
                'title': new_title,
            })
            return 'success'
        else:
            abort(403)
    else:
        abort(code)
