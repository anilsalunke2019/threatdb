# -*- coding: utf-8 -*-
"""
A database API for project
Created on 10/9/2019
@author: Anurag
"""

import time
import datetime
from sqlalchemy import create_engine

# third party imports
from common.config import conf
from api.views import BlockedIPsModel, MalwareURLsModel, RevisionTrackerModel, db


class ThreatDB:
    """
       A class for implementing database interacting functionality
    """

    def __init__(self):
        """
        Constructor
        """
        self.db_uri = conf.read().get('db-conf', 'DB_URI')
        self.engine = create_engine(self.db_uri)
        self.conn = self.engine.connect()

    def ip_remove_duplicates(self):
        """
        A sql to delete duplicate ip address record
        :return: None
        """
        query = """DELETE FROM blocked_ips WHERE id NOT IN
                (SELECT A.* FROM (SELECT MIN(id) FROM  blocked_ips GROUP BY ip_address)A);"""
        self.conn.execute(query)

    def url_remove_duplicates(self):
        """
        A sql to delete duplicate url record
        :return: None
        """
        query = """DELETE FROM malware_urls WHERE id NOT IN
                (SELECT A.* FROM (SELECT MIN(id) FROM  malware_urls GROUP BY url)A);"""
        self.conn.execute(query)

    def get_total_ip(self):
        """
        A sql query to get total count from ip table
        :return: query
        """
        total = BlockedIPsModel.query.count()
        return total

    def get_malware_count(self):
        """
        A sql query to get malware threat type count from the table
        :return:
        """
        malware = MalwareURLsModel.query.filter_by(threat_type='malware').count()
        return malware

    def get_phishing_count(self):
        """
        A sql query to get phishing threat type count from the table
        :return: query
        """
        phishing = MalwareURLsModel.query.filter_by(threat_type='phishing').count()
        return phishing

    def get_ransom_count(self):
        """
        A sql query to get ransomware threat type count from the table
        :return: query
        """
        ransom = MalwareURLsModel.query.filter_by(threat_type='ransomware').count()
        return ransom

    def get_total_url(self):
        """
        A sql query to get total count from url table
        :return: query
        """
        total = MalwareURLsModel.query.count()
        return total

    def write_first_revision_for_tracker(self):
        """
        A method to write revision for thr first time
        :return:
        """
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        rev = RevisionTrackerModel(last_revision=1, updated_at=timestamp)
        db.session.add(rev)
        db.session.commit()
