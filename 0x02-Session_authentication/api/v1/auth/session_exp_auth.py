#!/usr/bin/env python3
"""
    Contains class SessionExpAuth
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


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

    def create_session(self, user_id=None) -> str:
        """
            Creates a new session
        """
        sessionID = super().create_session(user_id)
        if sessionID is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[sessionID] = session_dictionary
        return sessionID

    def user_id_for_session_id(self, session_id=None) -> str:
        """
            returns a user_id
            for a particular sessionID
            if the session isn't expired
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if self.session_duration <= 0:
            return user_details.get('user_id')
        creation_time = user_details.get(
            'created_at')
        if creation_time is None:
            return None
        if (creation_time + timedelta(
                seconds=self.session_duration)) < datetime.now():
            return None
        return user_details.get('user_id')
