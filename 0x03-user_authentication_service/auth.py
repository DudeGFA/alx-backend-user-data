#!/usr/bin/env python3
"""
    authentication module
"""
import bcrypt


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
