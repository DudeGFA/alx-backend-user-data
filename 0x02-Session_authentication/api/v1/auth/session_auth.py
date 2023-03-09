#!/usr/bin/env python3
"""
    Contains class SessionAuth
"""
from .auth import Auth
from uuid import uuid4
from models.user import User
from typing import TypeVar
from os import getenv


class SessionAuth(Auth):
    """
        Implements session based
        authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        sessionID = str(uuid4())
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns a User instance
            based on a cookie value
            Args:
                request: request object
        """
        session_cookie = self.session_cookie(request)
        userID = self.user_id_by_session_id.get(session_cookie)
        return User.get(userID)

    def destroy_session(self, request=None):
        """
            deatroys a session
            returns True is session
            is destroyed else False
        """
        if request is None:
            return False
        session_ID = self.session_cookie(request)
        if session_ID is None:
            return False
        user_id = self.user_id_for_session_id(session_ID)
        if user_id is None:
            return False
        else:
            del self.user_id_by_session_id[session_ID]
            return True
