#!/usr/bin/env python3
"""
    Contains Class Auth
"""
from flask import request
from typing import List


class Auth():
    """
       Autentication class
       contains:
        function require_auth
        function authorization_header
        function current_user
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Checks if a user requires
            authentication
        """
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths or (
                path + '/') in excluded_paths or path[:-1] in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
            returns request authorization
            header
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Current user
        """
        return None
