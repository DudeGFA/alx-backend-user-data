#!/usr/bin/env python3
"""
     handles all routes for
     the Session authentication
"""
from flask import request, make_response, abort
from models.user import User
from os import getenv
from api.v1.views import app_views
import json


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - response object with session ID cookie
    """
    email = request.form.get('email')
    if email is None:
        return {"error": "email missing"}, 400
    password = request.form.get('password')
    if password is None:
        return {"error": "password missing"}, 400
    users = User.search({'email': email})
    if not users:
        return {"error": "no user found for this email"}, 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            sessionID = auth.create_session(user.id)
            resp = make_response(user.to_json())
            resp.set_cookie(getenv('SESSION_NAME'), sessionID)
            return resp

    return {"error": "wrong password"}, 401


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
        logs out a user
        by destroying a session
    Return:
      - empty json object
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return json.loads('{}'), 200
    else:
        abort(404)
