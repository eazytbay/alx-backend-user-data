#!/usr/bin/env python3
"""A view to handle all routes for Session based authentication"""

from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
import os
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_view():
    """A session based post view"""
    email = request.form.get('email')
    passw = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not passw:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    user = None
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for u in users:
        if u.is_valid_password(passw):
            user = u
    if user is None:
        return jsonify({"error": "wrong password"}), 401
    if user:
        from api.v1.app import auth
        sess = auth.create_session(user.id)
        resp = make_response(jsonify(user.to_json()))
        resp.set_cookie(os.getenv('SESSION_NAME', '_my_session_id'), sess)
        return resp


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
