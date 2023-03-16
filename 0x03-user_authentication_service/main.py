#!/usr/bin/env python3
import requests

def register_user(email: str, password: str) -> None:
    resp = requests.post('localhost:500/users', data = {'email': email, 'password': password})
    assert resp == {"message": "Bienvenue"}

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
