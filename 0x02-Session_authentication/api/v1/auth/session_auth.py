#!/usr/bin/env python3
"""
    Contains class SessionAuth
"""
from .auth import Auth
from uuid import uuid4


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
        sessionID = uuid4()
        user_id_by_session_id[sessionID] = user_id
        return sessionID
