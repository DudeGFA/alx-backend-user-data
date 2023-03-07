#!/usr/bin/env python3
"""
    Conatins class BasicAuth
"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
        Implements Basic authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            returns the Base64 part
            of the Authorization header
            for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
            returns the decoded value
            of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth_header = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return auth_header.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
             returns the user email and password
             from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        colon_idx = decoded_base64_authorization_header.index(':')
        username = decoded_base64_authorization_header[:colon_idx]
        password = decoded_base64_authorization_header[colon_idx + 1:]
        return username, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
            returns the User instance
            based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
            if user == [] or user is None or user == [None]:
                return None
            if not user[0].is_valid_password(user_pwd):
                return None
            else:
                return user[0]
        except Exception:
            return None
