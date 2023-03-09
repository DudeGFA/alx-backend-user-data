#!/usr/bin/env python3
"""
    Contains class SessionDBAuth
"""
from flask import request
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
        Implements session authentication
        but with expiry and session database storage
    """

    def create_session(self, user_id=None):
        """
            Craetes and stores new UserSession
            by it's sessionId
        """
        sessionID = super().create_session(user_id)
        if sessionID is None or not isinstance(self, str):
            return None
        kwargs = {'user_id': user_id, 'session_id': sessionID}
        new_session = UserSession(**kwargs)
        new_session.save()
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """
            returns a user_id
            for a particular sessionID
            if the session isn't expired
        """
        if session_id is None:
            return None
        try:
            user_details = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(user_details) <= 0:
            return None
        if self.session_duration <= 0:
            return user_details.get('user_id')
        creation_time = user_details[0].created_at
        if creation_time is None:
            return None
        if (creation_time + timedelta(
                seconds=self.session_duration)) < datetime.now():
            return None
        return user_details.user_id

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
        try:
            user_details = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(user_details) <= 0:
            return False
        else:
            user_details[0].remove()
            return True
