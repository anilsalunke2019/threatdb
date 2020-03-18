# -*- coding: utf-8 -*-
"""
Database models for this project
Created on 21/10/2019
@author: Anurag
"""

# imports
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def dump_datetime(value):
    """
    Deserialize datetime object into string form for JSON processing.
    :param value:
    :return:
    """

    if value is None:
        return None
    return value.strftime("%Y-%m-%d") + " " + value.strftime("%H:%M:%S")


class BlockedIPsModel(db.Model):
    """
    DB Model for blocked_ips table
    """
    __tablename__ = 'blocked_ips'
    id = db.Column('id', db.INTEGER, primary_key=True)
    ip_address = db.Column('ip_address', db.String(50), nullable=False)
    reliability = db.Column('reliability', db.INTEGER, nullable=True)
    priority = db.Column('priority', db.INTEGER, nullable=True)
    activity = db.Column('activity', db.String(128), nullable=True)
    sub_category = db.Column('sub_category', db.String(128), nullable=True)
    country = db.Column('country', db.String(128), nullable=True)
    city = db.Column('city', db.String(128), nullable=True)
    latitude = db.Column('latitude', db.FLOAT, nullable=True)
    longitude = db.Column('longitude', db.FLOAT, nullable=True)
    source = db.Column('source', db.String(128), nullable=True)
    target = db.Column('target', db.String(128), nullable=True)
    dest_port = db.Column('dest_port', db.INTEGER, nullable=True)
    last_online = db.Column('last_online', db.String(128), nullable=True)
    first_seen = db.Column('first_seen', db.String(128), nullable=True)
    used_by = db.Column('used_by', db.String(128), nullable=True)
    reference_link = db.Column('reference_link', db.String(128), nullable=True)
    created_at = db.Column('created_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = db.Column('updated_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    revision = db.Column('revision', db.INTEGER, nullable=False, default=0)

    def __init__(
            self, ip_address, reliability, priority, activity,
            sub_category, country, city, latitude, longitude, source,
            target, dest_port, last_online, first_seen, used_by, reference_link,
            created_at=None, updated_at=None, revision=None
    ):
        """
        Constructor
        """
        self.ip_address = ip_address
        self.reliability = reliability
        self.priority = priority
        self.activity = activity
        self.sub_category = sub_category
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.source = source
        self.target = target
        self.dest_port = dest_port
        self.last_online = last_online
        self.first_seen = first_seen
        self.used_by = used_by
        self.reference_link = reference_link
        self.created_at = created_at
        self.updated_at = updated_at
        self.revision = revision

    def __str__(self):
        """
        Object string representation
        :return:
        """
        return self.ip_address

    @property
    def serialize(self):
        """
        Return object data in easily serializable format
        :return:
        """
        output = {
            'id': self.id,
            'ip_address': self.ip_address,
            'reliability': self.reliability,
            'priority': self.priority,
            'activity': self.activity,
            'sub_category': self.sub_category,
            'country': self.country,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'source': self.source,
            'target': self.target,
            'dest_port': self.dest_port,
            'last_online': self.last_online,
            'first_seen': self.first_seen,
            'used_by': self.used_by,
            'reference_link': self.reference_link,
            'created_at': dump_datetime(self.created_at),
            'updated_at': dump_datetime(self.updated_at),
            'revision': self.revision,
        }
        return output


class MalwareURLsModel(db.Model):
    """
    DB model for malware url table
    """
    __tablename__ = 'malware_urls'
    id = db.Column('id', db.INTEGER, primary_key=True)
    url = db.Column('url', db.String(256), nullable=False)
    domain = db.Column('domain', db.String(256), nullable=True)
    filename = db.Column('filename', db.String(256), nullable=True)
    priority = db.Column('priority', db.String(256), nullable=True)
    file_type = db.Column('file_type', db.String(256), nullable=True)
    country = db.Column('country', db.String(256), nullable=True)
    url_status = db.Column('url_status', db.String(256), nullable=True)
    date_added = db.Column('date_added', db.String(256), nullable=True)
    threat_type = db.Column('threat_type', db.String(256), nullable=True)
    threat_tag = db.Column('threat_tag', db.String(256), nullable=True)
    created_at = db.Column('created_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = db.Column('updated_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __init__(
            self, url, domain, filename, file_type, priority, country, url_status,
            date_added, threat_type, threat_tag, created_at=None, updated_at=None
    ):
        """
        Constructor
        """
        self.url = url
        self.domain = domain
        self.filename = filename
        self.file_type = file_type
        self.priority = priority
        self.country = country
        self.url_status = url_status
        self.date_added = date_added
        self.threat_type = threat_type
        self.threat_tag = threat_tag
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """
        String representation
        :return:
        """
        return self.url

    @property
    def serialize(self):
        """
        Return object data in easily serializable format
        :return:
        """

        output = {
            'id': self.id,
            'url': self.url,
            'domain': self.domain,
            'filename': self.filename,
            'file_type': self.file_type,
            'priority': self.priority,
            'country': self.country,
            'url_status': self.url_status,
            'date_added': self.date_added,
            'threat_type': self.threat_type,
            'threat_tag': self.threat_tag,
            'created_at': dump_datetime(self.created_at),
            'updated_at': dump_datetime(self.updated_at),
        }
        return output


class RevisionTrackerModel(db.Model):
    """
    A database model for revision_tracker table
    """

    __tablename__ = 'revision_tracker'
    id = db.Column('id', db.INTEGER, primary_key=True)
    last_revision = db.Column('last_revision', db.INTEGER)
    created_at = db.Column('created_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = db.Column('updated_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __init__(self, last_revision, created_at=None, updated_at=None):
        """Constructor"""
        self.last_revision = last_revision
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """
        String representation
        :return:
        """
        return self.id


class AuthDataModel(db.Model):
    """
    A database model for client_details table
    """

    __tablename__ = 'client_details'
    id = db.Column('ID', db.INTEGER, primary_key=True)
    client_name = db.Column('client_name', db.VARCHAR(16), nullable=True)
    client_ip = db.Column('client_ip', db.VARCHAR(16), unique=True)
    api_key = db.Column('api_key', db.VARCHAR(256), unique=True)
    created_at = db.Column('created_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = db.Column('updated_at', db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __init__(self, client_name='Coder', client_ip=None, api_key=None, created_at=None, updated_at=None):
        """
        Constructor
        """
        self.client_name = client_name
        self.client_ip = client_ip
        self.api_key = api_key
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        """
        Object String representation
        :return:
        """
        return self.client_name
