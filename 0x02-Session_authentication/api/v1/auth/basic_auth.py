#!/usr/bin/env python3
"""
    Contains class BasicAuth
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
        return (username, password)

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
            users = User.search({'email': user_email})
            if users == [] or users is None or users == [None]:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            retrieves the User instance for a request
        """
        try:
            auth_header = self.authorization_header(request)
            if auth_header is not None:
                extr_ah = self.extract_base64_authorization_header(
                    auth_header)
                if extr_ah is not None:
                    decode = self.decode_base64_authorization_header(
                        extr_ah)
                    if decode is not None:
                        user_email, user_pwd = self.extract_user_credentials(
                            decode)
                        if user_email is not None:
                            return self.user_object_from_credentials(
                                user_email, user_pwd)
            return None
        except Exception:
            return None
