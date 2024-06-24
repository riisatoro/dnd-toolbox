from bcrypt import hashpw, gensalt

from database.connection import session, session_decorator
from database.models.users import User


@session_decorator
def is_user_exists(email: str) -> bool:
    return session.query(User).filter(User.email == email).first() is not None


@session_decorator
def create_new_user(fields: dict):
    fields['password'] = hashpw(fields['password'].encode("utf-8"), gensalt()).decode("utf-8")
    user = User(**fields)
    session.add(user)
    session.commit()
    return user


@session_decorator
def get_user_by_email(email: str) -> User:
    return (
        session.query(User)
        .filter(User.email == email)
        .first()
    )


@session_decorator
def get_users(item_id: int | None = None):
    query = session.query(User)
    if item_id:
        return query.filter(User.id == item_id).first()
    return query.all()


@session_decorator
def update_user(item_id: int, fields: dict):
    session.query(User).filter(User.id == item_id).update(fields)
    session.commit()
    return get_users(item_id)


@session_decorator
def delete_user(item_id: int):
    user = session.query(User).filter(User.id == item_id).first()
    session.delete(user)
    session.commit()
