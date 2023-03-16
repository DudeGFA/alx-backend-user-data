#!/usr/bin/env python3
"""
    flask app
"""
from flask import (
    Flask, jsonify, request, make_response, abort, redirect, url_for)
from auth import Auth
from user import User


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """
        returns JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        end-point to register a user
        return: JSON payload
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        end point to login a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        abort(401)
    if AUTH.valid_login(email, password):
        sessionID = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie('session_id', sessionID)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
        Logs out a user
        and destroys a session
    """
    sessionID = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sessionID)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
        returns a user's details
    """
    sessionID = request.cookies.get('session_id')
    if sessionID is None:
        abort(403)
    user = AUTH.get_user_from_session_id(sessionID)
    if user is not None:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
        gets a reset password token
        Args:
            emal: str - user's email
        return: JSON payload
    """
    email = request.form.get("email")
    if email is None:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
