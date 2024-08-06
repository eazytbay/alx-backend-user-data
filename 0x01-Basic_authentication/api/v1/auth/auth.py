#!/usr/bin/env python3
""" Authenticaton Module
"""
from flask import request
from typing import (List, TypeVar)


class Auth:
    """Authentication class"""

    def __init__(self):
        """Initialises an 'Auth' instance"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if @path needs authentication before allowing accessing
        """
        if (path is None or
                excluded_paths is None or
                type(excluded_paths) is list and len(excluded_paths) == 0):
            return True
        slash_tolerant = path[-1] == '/'
        if not slash_tolerant:
            path += '/'
        for x in excluded_paths:
            if x[-1] == '*':
                if path.startswith(x[:-1]):
                    return False
            if x == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None
        """
        if request is None:
            return None

        key_authorization = request.headers.get('Authorization', None)

        return key_authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None
        """
        return None
