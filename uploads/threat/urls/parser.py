# -*- coding: utf-8 -*-
"""
URLParser class for getting url information on given parameter.
Created on 10/9/2019
@author: Anurag
"""

# imports
import pathlib
import tldextract
from urllib.parse import urlparse


class URLParser:
    """
    A class for updating urls on parameters on domain, filename, file_type, threat_type
    """

    def __init__(self, url):
        """Constructor"""
        self._url = url
        self._parse = urlparse(self._url)
        self._ext = tldextract.extract(self._url)
        self._path = pathlib.Path(self._get_filepath())

    def get_domain(self):
        """
        Method to get domain name
        :return: domain in string
        """
        return self._ext.domain

    def _get_filepath(self):
        """
        Get file path if exists
        :return: file path in string
        """
        if len(self._parse.path) > 0:
            return self._parse.path
        else:
            return "NA"

    def get_filename(self):
        """
        Get file name from URL
        :return: filename in string
        """
        return self._path.name

    def get_filetype(self):
        """
        Get file type if filename exists
        :return: file type in string
        """
        if self.get_filename() == 'NA':
            return 'NA'
        else:
            return self._path.suffix.lstrip('.')

    def get_threat_type(self):
        """
        Get threat type depending on file existance
        :return: Phishing or Malware in string
        """
        if self._get_filepath() == 'NA':
            return 'phishing'
        else:
            return 'malware'
