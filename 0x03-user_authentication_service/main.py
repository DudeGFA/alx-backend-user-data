#!/usr/bin/env python3
"""
    Contains test functions for
    app.py
"""
import requests


def register_user(email: str, password: str) -> None:
    """
        tests POST /users endpoint
    """
    resp = requests.post(
        'http://172.17.0.21:5000//users',
        data={
            'email': email,
            'password': password})
    assert resp == {"message": "Bienvenue"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
