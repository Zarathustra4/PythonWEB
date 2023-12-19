from app.auth.models import UserModel
from app.exceptions import UserInputException
from ..extensions import db


def model_to_dict(model: UserModel):
    return {
        "username": model.username,
        "email": model.email,
        "about": model.about
    }


def find_all():
    users = UserModel.query.all()
    return list(map(model_to_dict, users))


def get_user_by_id(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    if user is None:
        raise UserInputException(f"There is no with a user with {user_id=}")

    return model_to_dict(user)


def create_user(body):
    username = body.get("username")
    email = body.get("email")
    about = body.get("about")
    password = body.get("password")

    if UserModel.query.filter_by(username=username).first() is not None:
        raise UserInputException("Username is taken")
    if UserModel.query.filter_by(email=email).first() is not None:
        raise UserInputException("Email is taken")

    user = UserModel(
        username=username,
        email=email,
        about=about
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return model_to_dict(user)


def delete_by_id(user_id: int):
    try:
        UserModel.query.filter_by(id=user_id).delete()
        db.session.commit()
    except Exception as e:
        raise UserInputException(str(e))


def update_by_id(user_id: int, body):
    username = body.get("username")
    email = body.get("email")
    about = body.get("about")
    password = body.get("password")
    new_password = body.get("new_password")

    user: UserModel = UserModel.query.filter_by(id=user_id).first()
    if user is None:
        raise UserInputException(f"There is no such user with {user_id=}")

    if not user.check_password(password):
        raise UserInputException("Wrong password")

    user.username = username if username else user.username
    user.email = email if email else user.email
    user.about = about if about else user.about
    if new_password:
        user.set_password(new_password)

    db.session.commit()

    return model_to_dict(user)
