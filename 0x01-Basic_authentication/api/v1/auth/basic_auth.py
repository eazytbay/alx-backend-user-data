#!/usr/bin/env python3
"""Module for Basic Auth"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar
import base64
import re
import binascii


class BasicAuth(Auth):
    """Basic Authentication Class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of @authorization_header for
        a Basic Authentication
        """
        if (authorization_header is None or
                type(authorization_header) is not str):
            return None
        auth_type = re.match("^(Basic )(.*)", authorization_header)
        if auth_type is None:
            return None
        auth_type = auth_type.groups()
        if auth_type[0] != "Basic ":
            return None

        return auth_type[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of @base64_authorization_header string
        """
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            dec_auth = base64_authorization_header.encode('utf-8')
            dec_auth = base64.b64decode(dec_auth)
            return dec_auth.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
                type(decoded_base64_authorization_header) is not str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        auth_info = re.match("^([^:]+):(.*)$",
                             decoded_base64_authorization_header)
        return (auth_info.groups())

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """Returns the 'User' instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        temp_user = User(email=user_email)
        users = temp_user.search({'email': user_email})
        if len(users) == 0:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]

      def current_user(self, request=None) -> TypeVar('User'):
        """Bombards 'Auth' to retrieve the 'User' instance for a request
        """
        auth_header = self.authorization_header(request)
        auth_token = self.extract_base64_authorization_header(auth_header)
        if auth_token is None:
            return None

        dec_auth = self.decode_base64_authorization_header(auth_token)
        user_credentials = self.extract_user_credentials(dec_auth)
        if user_credentials is None:
            return None
        return self.user_object_from_credentials(*user_credentials)
