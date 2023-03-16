#!/usr/bin/env python3
"""
    Contains test functions for
    app.py
"""
import requests


def register_user(email: str, password: str) -> None:
    """
        tests user regristration
        Args:
            email: User's email
            password: User's password
        Return: None
    """
    resp = requests.post(
        'http://172.17.0.21:5000//users',
        data={
            'email': email,
            'password': password})
    if resp.status_code == 200:
        assert (resp.json() == {"email": email, "message": "user created"})
    else:
        assert(resp.status_code == 400)
        assert(resp.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
        tests user login
        with a wrong password
        Args:
            email: User's email
            password: wrong User's password
        Return: None
    """
    resp = requests.post(
        'http://127.0.0.1:5000/sessions',
        data={
            'email': email,
            'password': password})
    assert (resp.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
        tests user login
        with the right password
        Args:
            email: User's email
            password: right User's password
        Return: The session ID
    """
    resp = requests.post(
        'http://127.0.0.1:5000/sessions',
        data={
            'email': email,
            'password': password})
    assert(resp.status_code == 200)
    assert(resp.json() == {"email": email, "message": "logged in"})
    return resp.cookies['session_id']


def profile_unlogged() -> None:
    """
        tries to get user's profile
        while not logged in
    """
    resp = requests.get(
        'http://127.0.0.1:5000/profile')
    assert (resp.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
        tries to get user's profile
        while logged in
        Args:
            session_id: str - session ID
    """
    resp = requests.get(
        'http://127.0.0.1:5000/profile',
        cookies={'session_id': session_id})
    assert (resp.status_code == 200)


def log_out(session_id: str) -> None:
    """Tests log out
    Args:
        session_id: str - session ID
    """
    resp = requests.delete(
        'http://127.0.0.1:5000/sessions',
        cookies={'session_id': session_id})
    if resp.status_code == 302:
        assert(resp.url == 'http://127.0.0.1:5000/')
    else:
        assert(resp.status_code == 200)


def reset_password_token(email: str) -> str:
    """
        Tests generation of
        password reset token
        Args:
            email: User's email
        Rerturn: reset token
    """
    resp = requests.post(
        'http://127.0.0.1:5000/reset_password',
        data={'email': email})
    assert resp.status_code == 200
    return resp.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
        Tests password update
        Args:
            email: str - User's email
            reset_token: str - The password reset token
            new_password: str - User's new password
        Returns: None
    """
    resp = requests.put(
        'http://127.0.0.1:5000/reset_password',
        data={'email': email, 'reset_token': reset_token,
              'new_password': new_password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
