#!/usr/bin/env python3
"""
    Contains class UserSession
"""
from base import Base


class UserSession(Base):
    """
        Class user session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
            initialise new instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
