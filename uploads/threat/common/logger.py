# -*- coding: utf-8 -*-
"""
A customised logger for this project for logging to the file and console
Created on 10/9/2019
@author: Anurag
"""

# imports
import os
import logging

# local imports
from common.config import conf


class Logger:
    """
    A Threat intelligence hub logger which will take care
    of logging to console and file.
    """

    def __init__(self, filepath):
        """
        Constructor
        :param filepath:
        """
        self.filepath = filepath
        self.logger = logging.getLogger('THREAT-HUB')
        self.logger.setLevel(logging.DEBUG)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # file handler
        file_handller = logging.FileHandler(os.path.join(self.filepath))
        file_handller.setLevel(logging.DEBUG)
        file_handller.setFormatter(self._formatter)
        self.logger.addHandler(file_handller)
        # console handler
        con_handler = logging.StreamHandler()
        con_handler.setLevel(logging.ERROR)
        con_handler.setFormatter(self._formatter)
        self.logger.addHandler(con_handler)


log_file = conf.read().get('Other', 'LOG_FILE')
logger = Logger(log_file).logger
