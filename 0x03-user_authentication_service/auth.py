#!/usr/bin/env python3
"""Password hashing method"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from typing import TypeVar
from user import User


def _hash_password(password: str) -> str:
    """Accepts the password and returns bytes of a salted hash"""
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass.decode('utf-8')


def _generate_uuid() -> str:
    """ This function generates uuid"""
    _uuid = uuid4()
    return str(_uuid)


class Auth:
    """An Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registeration of a user and validating the user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password = _hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=passw)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """checks if the required arguments are valid login details"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password.encode('utf-8'))
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates and returns the created session ID"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id
                self._db._session.commit()
                return session_id
            else:
                raise ValueError

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """a method that receives a single session_id string argument
        and returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """This method takes in  a single user_id integer argument
        and returns None after destroying the session
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """This method takes in an email string argument
        and returns the user’s reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token_reset = _generate_uuid()
                user.token_reset = token_reset
                self._db._session.commit()
                return token_reset
            else:
                raise ValueError()
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """This is a method that takes in token_reset string argument
        and a password string argument to update the password
        in the db
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hshd_password = _hash_password(password)
                user.hshd_password = hshd_password
                user.token_reset = None
                self._db._session.commit()
            else:
                raise ValueError
        except NoResultFound:
            raise ValueError
