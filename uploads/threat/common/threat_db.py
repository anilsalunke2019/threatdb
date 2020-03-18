# -*- coding: utf-8 -*-
"""
THIS MODULE IS NOT LONGER IN USE
A database API for project
Created on 10/9/2019
@author: Anurag
"""

# global imports
import sys

# third party imports
try:
    from mysql.connector import connect
    from mysql.connector.errors import ProgrammingError, DatabaseError, InterfaceError, OperationalError
except ImportError:
    sys.exit("You need python mysql connector module installed")

# local imports
from common.logger import logger


class ThreatDB:
    """
    A class for implementing database interacting functionality
    """
    def __init__(self, host, database, user, password, table_name):
        self._host = host
        self._database = database
        self._user = user
        self._password = ""
        self.table_name = table_name
        if password is not None:
            self._password = password
        self._conn = None
        self._connected = False

    def connect(self):
        """
        Method to connect with MySQL database
        :return: connection object
        """
        try:
            self._conn = connect(host=self._host, database=self._database, user=self._user, password=self._password, use_pure=False)
            self._conn.autocommit = True
            self._connected = True
            logger.info("Database connection successful")
        except Exception as e:
            logger.info("Can't connect to database (%s@%s) error: %s" % (self._user, self._host, e))
        return self._conn

    def exec_query(self, query, params=None):
        """
        Method to execute given database query
        :param query: SQL query in string
        :param params: optional parameters for wuery
        :return: None
        """
        try:
            if not self._connected or self._conn is None:
                self.connect()
            cursor = self._conn.cursor()
            cursor.execute(query, params)
            return cursor
        except OperationalError as err:
            logger.debug('MySQL Operational Error executing query:\n----> %s \n----> %s' % (query, err))
            if err != 2006:
                logger.error('MySQL Operational Error executing query')
        except Exception as e:
            logger.error('Error executing query:\n----> [{0}]'.format(e))

    def close(self):
        """Method to close mysql database connection"""
        if self._conn:
            try:
                self._conn.close()
                logger.info("Database connection closed")
            except ProgrammingError as err:
                logger.error("Error while closing the connection: {}".format(err))
            except AttributeError as err:
                logger.info("Trying to close the connection to mysql: {}".format(err))
            except Exception as err:
                logger.error("Can't close the connection to the database: {}".format(err))
            finally:
                self._conn = None
                self._connected = False
        else:
            logger.info("Trying to execute close method on connection which doesn't exist")

    def ip_insert(self):
        """
        sql insert query for ip address module
        :return: query in string
        """
        query = """INSERT INTO blocked_ips (ip_address, reliability, priority, activity, sub_category, country, 
                city, latitude, longitude, source, target, dest_port, last_online, first_seen, used_by, reference_link
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        return query

    def url_insert(self):
        """
        sql insert query for url address module
        :return: query in string
        """
        query = """INSERT INTO malware_urls (url, domain, filename, file_type, priority, country, url_status, 
                date_added, threat_type, threat_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        return query

    def ip_update(self):
        """
        sql update query for ip address module
        :return: query in string
        """
        query = """UPDATE blocked_ips SET reliability = %s, priority = %s, activity = %s, sub_category = %s,
                   country = %s, city = %s, latitude = %s, longitude = %s, source = %s, target = %s, dest_port = %s,
                   last_online = %s, first_seen = %s, used_by = %s, reference_link = %s,
                   updated_at = %s WHERE ip_address = %s;"""
        return query

    def url_update(self):
        """
        sql update query for url address module
        :return: query in string
        """
        query = """UPDATE malware_urls SET `domain` = %s, filename = %s, file_type = %s, priority = %s, country = %s, 
                         url_status = %s, date_added = %s, threat_type = %s, threat_tag = %s, updated_at = %s WHERE url = %s;"""
        return query

    def ip_remove_duplicates(self):
        """
        A sql to delete duplicate ip address record
        :return: None
        """
        query = """DELETE FROM blocked_ips WHERE id NOT IN
                (SELECT A.* FROM (SELECT MIN(id) FROM  blocked_ips GROUP BY ip_address)A);"""
        self.exec_query(query)

    def url_remove_duplicates(self):
        """
        A sql to delete duplicate url record
        :return: None
        """
        query = """DELETE FROM malware_urls WHERE id NOT IN
                (SELECT A.* FROM (SELECT MIN(id) FROM  malware_urls GROUP BY url)A);"""
        self.exec_query(query)

    def get_total_ip(self):
        """
        A sql query to get total count from ip table
        :return: query
        """
        query = """SELECT COUNT(1) FROM blocked_ips;"""
        result = self.exec_query(query).fetchall()[0][0]
        return int(result)

    def get_malware_count(self):
        """
        A sql query to get malware threat type count from the table
        :return:
        """
        query = """SELECT COUNT(1) FROM malware_urls WHERE threat_type='Malware';"""
        result = self.exec_query(query).fetchall()[0][0]
        return int(result)

    def get_phishing_count(self):
        """
        A sql query to get phishing threat type count from the table
        :return: query
        """
        query = """SELECT COUNT(1) FROM malware_urls WHERE threat_type='Phishing'"""
        result = self.exec_query(query).fetchall()[0][0]
        return int(result)

    def get_ransom_count(self):
        """
        A sql query to get ransomware threat type count from the table
        :return: query
        """
        query = """SELECT COUNT(1) FROM malware_urls WHERE threat_type='Ransomware'"""
        result = self.exec_query(query).fetchall()[0][0]
        return int(result)

    def get_total_url(self):
        """
        A sql query to get total count from url table
        :return: query
        """
        query = """SELECT COUNT(1) FROM malware_urls;"""
        result = self.exec_query(query).fetchall()[0][0]
        return int(result)
