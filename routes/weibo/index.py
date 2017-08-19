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
from models.post import Post
from models.reply import Reply
from models.user import User

from routes import (
    current_user,
    validate_login_and_token_with_form,
    csrf_token,
    get_valid_with_form,
)
import uuid
import pymongo

main = Blueprint('weibo', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.register'))
    else:
        token = str(uuid.uuid4())
        csrf_token[token] = u.id
        post_list = Post().find_all(__sort=[('created_time', pymongo.DESCENDING)])
        # too sick
        for p in post_list:
            tmp_user = User().find_one(id=p.user_id)
            p.username = tmp_user.username
            p.user_image = tmp_user.user_image
            p.forward_id = p.id
            if p.refer_post_id != -1:
                p.set_attr_by_refer_post()
                p.forward_id = p.refer_post_id
        return render_template('weibo/index.html', token=token, post_list=post_list, user=u)


@main.route('/user')
def user():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_token[token] = u.id
    visit_user_id = int(request.args.get('user_id', -1))
    visit_user = User().find_one(id=visit_user_id)
    if u is not None and visit_user is not None:
        post_list = Post().find_all(user_id=visit_user_id, __sort=[('created_time', pymongo.DESCENDING)])
        # too sick
        for p in post_list:
            tmp_user = User().find_one(id=p.user_id)
            p.username = tmp_user.username
            p.user_image = tmp_user.user_image
            p.forward_id = p.id
            if p.refer_post_id != -1:
                p.set_attr_by_refer_post()
                p.forward_id = p.refer_post_id
        print(post_list)
        return render_template('weibo/user_post.html', token=token, post_list=post_list, user=u)
    return abort(403)


@main.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        u = current_user()
        token = str(uuid.uuid4())
        csrf_token[token] = u.id

        post_id = int(request.args.get('post_id', -1))
        post = Post().find_one(id=post_id)
        if u is not None and post is not None:
            tmp_user = User().find_one(id=post.user_id)
            post.username = tmp_user.username
            post.user_image = tmp_user.user_image
            post.forward_id = post.id
            if post.refer_post_id != -1:
                post.set_attr_by_refer_post()
                post.forward_id = post.refer_post_id
            reply_list = Reply().find_all(post_id=post_id, __sort=[('created_time', pymongo.DESCENDING)])
            for r in reply_list:
                tmp_user = User().find_one(id=r.user_id)
                r.user = tmp_user
            return render_template('weibo/post.html', token=token, p=post, reply_list=reply_list, user=u)
    else:
        code, u = validate_login_and_token_with_form(request)
        if code == 200:
            Post().new(request.form, user_id=u.id)
            return redirect(url_for('weibo.index'))
    return abort(403)


@main.route('/reply', methods=['POST'])
def reply():
    code, u = validate_login_and_token_with_form(request)
    post_id = int(request.form.get('post_id', -1))
    if code == 200 and Post().has(id=post_id):
        form = request.form.copy()
        form['user_id'] = u.id
        Reply.new(form)
        return redirect(url_for('.post', post_id=post_id))
    return abort(403)


@main.route('/forward', methods=['GET', 'POST'])
def forward():
    if request.method == 'GET':
        u = current_user()
        token = str(uuid.uuid4())
        csrf_token[token] = u.id
        refer_post_id = int(request.args.get('refer_post_id', -1))
        if u is not None:
            return render_template('weibo/forward.html', token=token, user=u, refer_post_id=refer_post_id)
    else:
        code, u = validate_login_and_token_with_form(request)
        print(request.form.get('refer_post_id'))
        refer_post_id = int(request.form.get('refer_post_id', -1))
        if code == 200 and Post().has(id=refer_post_id):
            Post().new(request.form)
            return redirect(url_for('.user', user_id=u.id))
    return abort(403)

    # code, u = validate_login_and_token_with_form(request)
    # post_id = int(request.form.get('post_id', -1))
    # if code == 200 and Post().has(id=post_id):
    #     form = request.form.copy()
    #     form['user_id'] = u.id
    #     Reply.new(form)
    #     return redirect(url_for('.post', post_id=post_id))
    # return abort(403)
