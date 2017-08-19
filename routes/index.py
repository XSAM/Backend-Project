from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
)
from models.user import User

from werkzeug.utils import secure_filename
from config import user_file_director
import os
from routes import (
    current_user,
    Valid,
    get_valid_with_form,
    validate_login_and_token_with_form,
    csrf_token,
)
from utils import log
import uuid

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
            return redirect(url_for('.index'))


@main.route('/logout')
def logout():
    u = current_user()
    if u is not None:
        session.clear()
    return redirect(url_for('.index'))


@main.route('/profile')
def profile():
    valid = get_valid_with_form(request)
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        token = str(uuid.uuid4())
        csrf_token[token] = u.id
        return render_template('profile.html', token=token, user=u, page_header=valid.page_header)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/add-user-image', methods=['POST'])
def add_user_image():
    code, u = validate_login_and_token_with_form(request)
    if code == 200:
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if allow_file(file.filename):
            filename = secure_filename(file.filename)

            # change pic name
            name, extension = os.path.splitext(filename)
            new_filename = str(u.id) + extension

            file.save(os.path.join(user_file_director, new_filename))
            u.user_image = new_filename
            u.save()
        return redirect(url_for('.profile'))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)