#!/usr/bin/env python3
"""
    authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
            initialises new instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user
            Args:
                email: str
                password: str
            return: new user object
                    if email isn't already reguistered
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
            Checks if a users login credentials
            are valid
            Returns: True if valid
                     False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            pw_bytes = password.encode('utf-8')
            return bcrypt.checkpw(pw_bytes, user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid() -> str:
        """
            returns a string representation of a new UUID
        """
        return str(uuid4())


def _hash_password(password: str) -> bytes:
    """
        Args:
            password: string
        Return: bytes
                The returned bytes is a salted
                hash of the input password
    """
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash
