# -*- coding: utf-8 -*-
"""
A authenticator class to implement token based authentication in API
Created on 21/10/2019
@author: Anurag
"""

# imports
import jwt
from functools import wraps

# local imports
from api.models import AuthDataModel


class Authenticator:
    """
    A class for implementing JWT authentication
    """

    def __init__(self, request=None):
        """
        Constructor
        :param request: flask request object
        """
        self.request = request
        self.secret = 'Hakuna-matata'
        self.algorithm = 'HS256'

    def get_remote_ip(self):
        """
        A method for taking requesting client IP address
        :return:
        """
        return self.request.remote_addr

    def create_token(self, identity):
        """
        A customised JWT token creation
        :param identity:
        :return: encoded token with jwt
        """
        try:
            token = jwt.encode({'identity': identity}, key=self.secret, algorithm=self.algorithm)
            return token
        except Exception as err:
            pass

    def decode_token(self, token):
        """
        Method to decode passed token
        :param token:
        :return: decoded value in key value pain
        """
        try:
            identity = jwt.decode(token, self.secret, self.algorithm)
            return identity
        except Exception as err:
            pass

    def verify_token(self, req_token, ip_address):
        """
        Method for verifying passed token with ip_address provided
        :param req_token:
        :param ip_address:
        :return: boolean
        """
        identity = self.decode_token(req_token)
        if identity is not None:
            if identity.get('identity') == ip_address:
                return True
        return False

    def token_required(self, func):
        """
        A decorator to use with every request
        :param func: api view function
        :return:
        """
        @wraps(func)
        def inner():
            ip = self.get_remote_ip()
            result = AuthDataModel.query.filter_by(client_ip=ip).first()
            if not result:
                return {'error': 'Please register', 'url': self.request.host_url + 'api/register'}
            else:
                header = self.request.headers.get('Authorization')
                if not header:
                    return {'error': "Missing Authorization Header"}
                else:
                    if self.verify_token(header.encode(), ip):
                        return func()
                    else:
                        return {'error': "Invalid access key"}
        return inner
