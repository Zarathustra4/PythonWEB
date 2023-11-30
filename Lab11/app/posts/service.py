import os

from werkzeug.utils import secure_filename

from app.posts.forms import CreatePostForm
from app.posts.models import PostModel
from datetime import datetime
from flask_login import current_user

import config
from ..extensions import db


def create_post(post_form: CreatePostForm):
    date = datetime.now().date()
    user_id = current_user.get_id()

    image = post_form.image.data

    filename = secure_filename(image.filename)
    image.save(os.path.join(
        config.basedir, 'app', 'static', 'posts', 'images', filename
    ))

    post = PostModel(title=post_form.title.data,
                     text=post_form.text.data,
                     image=filename,
                     created=date,
                     post_type=post_form.post_type.data,
                     user_id=user_id)

    db.session.add(post)
    db.session.commit()
