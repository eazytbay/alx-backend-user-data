#!/usr/bin/env python3
"""Session auth"""


from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """Handling Sessions as an authentication"""
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a given user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        sess_id = uuid.uuid4()
        self.user_id_by_session_id[str(sess_id)] = user_id
        return str(sess_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User Id based on a session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User insance based on the cookie value"""
        U_id = self.user_id_for_session_id(self.session_cookie(request))
        usr = User.get(U_id)
        return usr

    def destroy_session(self, request=None):
        """Destroys an authenticated session.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
