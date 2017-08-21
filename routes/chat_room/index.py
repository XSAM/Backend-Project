from flask import (
    session,
    redirect,
    url_for,
    render_template,
    request,
    Blueprint,
)
from routes import (
    current_user,
    get_valid_with_form,
)

main = Blueprint('chat_room', __name__)


@main.route('/', methods=['GET'])
def index():
    # if request.form.get('name') is not None:
    #     session['name'] = request.form['name']
    #     return redirect(url_for('.chat'))
    # elif request.method == 'GET':
    valid = get_valid_with_form(request)
    return render_template('chat_room/index.html', page_header=valid.page_header)

