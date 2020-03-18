# -*- coding: utf-8 -*-
"""
A Crawler for getting response from endpoints and convert them to JSON
Created on 10/9/2019
@author: Anurag
"""
# imports
import requests
import time

# local imports
from common.logger import logger
from common.targets import ip_targets, url_targets
from common.config import conf


class Crawler:
    """
    A Crawler class with required methods for getting response data from given url
    """

    def __init__(self):
        """Constructor"""
        self.parser = conf.read().get('Host', 'parser_url')
        self.ip_targets = ['http://' + x + y for x in self.parser for y in ip_targets]
        self.url_targets = ['http://' + x + y for x in self.parser for y in url_targets]
        self._ip_length = len(self.ip_targets)

    @property
    def total_urls(self):
        """
        A method to get total ip urls count
        :return:
        """
        return self._ip_length

    @staticmethod
    def send_request(url):
        """
        A method for sending request to argument url and return the text response
        :param url: http endpoint
        """
        max_retries = 2
        timeout = 45
        while max_retries > 0:
            try:
                logger.info("Requesting url - {}".format(url))
                response = requests.get(url=url, timeout=timeout)
                if response.status_code == 200:
                    logger.info("Response fetched from url - {}".format(url))
                    return response.json()
            except Exception as err:
                logger.exception("Could not fetch response from {} - {}".format(url, err), exc_info=False)
                if not max_retries == 1:
                    logger.info("Retrying in 2 seconds...")
                time.sleep(2)
            max_retries -= 1
