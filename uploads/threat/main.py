# -*- coding: utf-8 -*-
"""
A main run module for the project
Created on 21/10/2019
@author: Anurag
"""

# imports
from ip_address.ipdriver import IPDriver
from urls.urldriver import URLDriver
from common.splash import threat_hub


if __name__ == '__main__':
    print(threat_hub)
    IPDriver().ip_main()
    URLDriver().url_main()
