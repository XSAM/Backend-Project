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
    validate_login_and_token_with_form,
    csrf_token,
    get_valid_with_form,
)
import uuid

main = Blueprint('todo', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.register'))
    else:
        token = str(uuid.uuid4())
        csrf_token[token] = u.id
        todo_list = Todo.cache_by_user_id(u.id)
        valid = get_valid_with_form(request)
        # return render_template('todo/tmp.html', page_header=valid.page_header)
        return render_template('todo/index.html', token=token, todo_list=todo_list, page_header=valid.page_header)


@main.route('/add', methods=['POST'])
def add():
    code = validate_login_and_token_with_form(request)
    title = request.form.get('title', '')
    if code == 200:
        u = current_user()
        log('User: {},Add todo,Title: {}'.format(u.id, title))
        Todo().new({
            'user_id': u.id,
            'title': title,
        })
        return redirect(url_for('.index'))
    else:
        abort(code)


@main.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    code = validate_login_and_token_with_form(request)
    title = request.form.get('title', '')
    if code == 200:
        u = current_user()
        t = Todo.find_one(id=todo_id)
        if t.user_id == u.id:
            log('User: {},Edit todo,before Title: {}, after Title: {}'.format(u.id, t.title, title))
            t.update({
                'title': title,
            })
            return redirect(url_for('.index'))
        else:
            abort(403)
    else:
        abort(code)


@main.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    print(request.form)
    code = validate_login_and_token_with_form(request)
    if code == 200:
        u = current_user()
        t = Todo.find_one(id=todo_id)
        if t.user_id == u.id:
            log('User: {},Delete todo,Title: {},'.format(u.id, t.title))
            t.delete()
            return redirect(url_for('.index'))
        else:
            abort(403)
    else:
        abort(code)
