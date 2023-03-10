from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from app.models import (
    Role,
    RoleCreate,
    PasswordChange,
    User,
    UserCreate,
    UserUpdate,
)
from app.security import auth_exception, hash_password, verify_password


def select_users(session: Session) -> List[User]:
    query = select(User)
    return session.execute(query).scalars().all()


def insert_user(user: UserCreate, session: Session) -> User:
    user_db = User(**user.dict(exclude_unset=True, exclude={"role_ids"}))
    user_db.password = hash_password(user.password)
    for role_id in user.role_ids:
        try:
            role = select_role_by_id(role_id, session)
            user_db.roles.append(role)
        except NoResultFound:
            pass
    session.add(user_db)
    session.commit()

    return user_db


def select_user_by_id(user_id: int, session: Session) -> User:
    query = select(User).where(User.id == user_id)
    return session.execute(query).scalar_one()


def select_user_by_username(username: str, session: Session) -> User:
    query = select(User).where(User.username == username)
    return session.execute(query).scalar_one()


def update_user(user_id: int, user_data: UserUpdate, session: Session) -> User:
    user_db = select_user_by_id(user_id, session)
    for field, value in user_data.dict(exclude_none=True).items():
        if field == "role_ids":
            user_db.roles = []
            for role_id in value:
                try:
                    role = select_role_by_id(role_id, session)
                    user_db.roles.append(role)
                except NoResultFound:
                    pass
        else:
            setattr(user_db, field, value)
    session.commit()

    return user_db


def update_password(
    user_id: int, change_password_data: PasswordChange, session: Session
) -> User:
    user_db = select_user_by_id(user_id, session)
    if not verify_password(change_password_data.old_password, user_db.password):
        raise auth_exception("Invalid password")
    user_db.password = hash_password(change_password_data.new_password)
    session.commit()

    return user_db


def select_roles(session: Session) -> List[Role]:
    query = select(Role)
    return session.execute(query).scalars().all()


def select_role_by_id(role_id: int, session: Session) -> Role:
    query = select(Role).where(Role.id == role_id)
    return session.execute(query).scalar_one()


def insert_role(role: RoleCreate, session: Session) -> Role:
    role_db = Role(**role.dict(exclude_unset=True))
    session.add(role_db)
    session.commit()

    return role_db

