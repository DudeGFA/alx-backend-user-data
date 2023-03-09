#!/usr/bin/env python3
"""
    Contains class SessionExpAuth
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """
        Implements session authentication
        but with expiry as an added feature
    """

    def __init__(self):
        """
            Initializes class
            assigns instance variable session_duration
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
            Creates a new session
        """
        sessionID = super().create_session(user_id)
        if sessionID is None:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[sessionID] = session_dict
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """
            returns a user_id
            for a particular sessionID
            if the session isn't expired
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id].get('user_id')
        creation_time = self.user_id_by_session_id[session_id].get(
            'created_at')
        if creation_time is None:
            return None
        if (creation_time + self.session_duration) < datetime.now():
            return None
        return user_id_by_session_id[session_id].get('user_id')
