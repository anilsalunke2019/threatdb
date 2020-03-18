# -*- coding: utf-8 -*-
"""
Global variables for project level configuration
Created on 10/9/2019
@author: Anurag
"""

# imports
import os

from configparser import ConfigParser


class ConfigReader:
    """
    A class to implement custom cfg file reader
    """

    def __init__(self):
        self.cfg_file = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/setup.cfg')
        self._config = ConfigParser()
        self._config.read(self.cfg_file)

    def read(self):
        """
        A read method to read key and values
        :return:
        """
        return self._config


conf = ConfigReader()
