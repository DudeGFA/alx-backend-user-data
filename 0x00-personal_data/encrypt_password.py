#!/usr/bin/env python3
"""
    Contains:
        Function hash_password
        Fuction is_valid
"""
import bycrypt


def hash_password(password):
    """
        Args:
            password: str
        return: salted, hashed password
    """
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Args:
            hashed_password: encryped password
            password: str
        returns: true if hashed_password
                    matches password
    """
    if bcrypt.checkpw(password, hashed_password):
        return True
    else:
        return False
