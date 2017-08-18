from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    session,
)
from models.user import User

from routes import (
    current_user,
    Valid,
    get_valid_with_form,
)
from utils import log

main = Blueprint('index', __name__)


@main.route('/')
def index():
    valid = get_valid_with_form(request)
    return render_template('index.html', page_header=valid.page_header)


# TODO already login to get this route
@main.route('/register', methods=['GET', 'POST'])
def register():
    valid = get_valid_with_form(request)
    if request.method == 'GET':
        return render_template('register.html', page_header=valid.page_header)
    else:
        form = request.form
        u = User.register(form)
        # TODO
        if u is not None:
            # auto login
            session['user_id'] = u.id
            session.permanent = True
            return redirect(url_for('.index'))
        else:
            return render_template('register.html', page_header=valid.page_header)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        valid = get_valid_with_form(request)
        return render_template('login.html', page_header=valid.page_header)
    else:
        form = request.form
        u = User.validate_login(form)
        print(u)
        if u is None:
            # login fail
            return redirect(url_for('.index'))
        else:
            # login success
            session['user_id'] = u.id
            session.permanent = True
            return redirect(url_for('todo.index'))


@main.route('/logout')
def logout():
    u = current_user()
    if u is not None:
        session.clear()
    return redirect(url_for('.index'))
