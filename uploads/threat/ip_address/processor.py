# -*- coding: utf-8 -*-
"""
A central processor for database insert / update logic
Created on 10/9/2019
@author: Anurag
"""

import time
import datetime

# imports
import pandas as pd
from geoip2.errors import AddressNotFoundError

# local imports
from common.logger import logger
from common.threat_orm import ThreatDB
from common.config import conf
from ip_address.location_updater import LocationUpdater
from ip_address.revision_tracker import RevisionTracker
from api.views import BlockedIPsModel, db


class Processor:
    """
    A class for processing input data and for inserting / updating the database
    """

    def __init__(self, chunk_size=None):
        self._dataset = pd.DataFrame()
        self._updated_df = pd.DataFrame()
        self.chunk_size = chunk_size
        self.db = ThreatDB()
        self.revision = RevisionTracker()

    def shape_up(self, raw_data):
        """
        A method for preparing pandas self.dataset from raw JSON
        :param raw_data: A input JSON data from URL response.
        :return: Pandas self.dataset
        """
        try:
            dataset = self._dataset.from_dict(raw_data, orient='index')
            dataset.reset_index(level=0, inplace=True)
            dataset.rename(columns={
                'index': 'ip_address', 'first_seeen': 'first_seen', 'lat': 'latitude', 'long': 'longitude'
            }, inplace=True)
            dataset.drop_duplicates(subset='ip_address', keep='first', inplace=True)
            dataset['ip_address'] = dataset['ip_address'].astype('str')
            dataset['reliability'] = dataset['reliability'].astype('int')
            dataset['priority'] = dataset['priority'].astype('int')
            dataset['latitude'] = dataset['latitude'].astype('float')
            dataset['longitude'] = dataset['longitude'].astype('float')
            dataset['dest_port'] = dataset['dest_port'].astype('int')
            dataset['last_online'] = dataset['last_online'].astype('str')
            dataset['first_seen'] = dataset['first_seen'].astype('str')
            dataset['revision'] = 0
            return dataset
        except Exception as err:
            logger.exception(err)

    def insert_db(self, dataset):
        """
        A method to insert pandas dataframe into database
        :return: None
        """
        ip_address = dataset['ip_address'].values
        reliability = dataset['reliability'].values
        priority = dataset['priority'].values
        activity = dataset['activity'].values
        sub_category = dataset['sub_category'].values
        country = dataset['country'].values
        city = dataset['city'].values
        latitude = dataset['latitude'].values
        longitude = dataset['longitude'].values
        source = dataset['source'].values
        target = dataset['target'].values
        dest_port = dataset['dest_port'].values
        last_online = dataset['last_online'].values
        first_seen = dataset['first_seen'].values
        used_by = dataset['used_by'].values
        reference_link = dataset['reference_link'].values
        for i in range(len(dataset)):
            try:
                record = BlockedIPsModel(
                    ip_address=str(ip_address[i]),
                    reliability=int(reliability[i]),
                    priority=int(priority[i]),
                    activity=str(activity[i]),
                    sub_category=str(sub_category[i]),
                    country=str(country[i]),
                    city=str(city[i]),
                    latitude=float(latitude[i]),
                    longitude=float(longitude[i]),
                    source=str(source[i]),
                    target=str(target[i]),
                    dest_port=int(dest_port[i]),
                    last_online=str(last_online[i]),
                    first_seen=str(first_seen[i]),
                    used_by=str(used_by[i]),
                    reference_link=str(reference_link[i]),
                    revision=self.revision.current_revision
                )
                db.session.add(record)
                db.session.commit()
            except Exception as err:
                logger.exception(err)
                db.session.rollback()

    @staticmethod
    def flush_db():
        """
        A method to truncate blocked_ips table
        """
        try:
            BlockedIPsModel.query.delete()
            db.session.commit()
        except Exception as err:
            logger.exception(err)

    def commit_changes(self, dataset):
        """
        A method for actually commiting changes to the database
        :param dataset: difference dataFrame
        :return: None
        """
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        ip_address = dataset['ip_address'].values
        reliability = dataset['reliability'].values
        priority = dataset['priority'].values
        activity = dataset['activity'].values
        sub_category = dataset['sub_category'].values
        country = dataset['country'].values
        city = dataset['city'].values
        latitude = dataset['latitude'].values
        longitude = dataset['longitude'].values
        source = dataset['source'].values
        target = dataset['target'].values
        dest_port = dataset['dest_port'].values
        last_online = dataset['last_online'].values
        first_seen = dataset['first_seen'].values
        used_by = dataset['used_by'].values
        reference_link = dataset['reference_link'].values
        for i in range(len(dataset)):
            BlockedIPsModel.query.filter_by(ip_address=str(ip_address[i])).update(
                dict(
                    reliability=int(reliability[i]),
                    priority=int(priority[i]),
                    activity=str(activity[i]),
                    sub_category=str(sub_category[i]),
                    country=str(country[i]),
                    city=str(city[i]),
                    latitude=float(latitude[i]),
                    longitude=float(longitude[i]),
                    source=str(source[i]),
                    target=str(target[i]),
                    dest_port=int(dest_port[i]),
                    last_online=str(last_online[i]),
                    first_seen=str(first_seen[i]),
                    used_by=str(used_by[i]),
                    reference_link=str(reference_link[i]),
                    updated_at=timestamp,
                    revision=self.revision.current_revision
                ))

            db.session.commit()

    def get_unique(self, response_df):
        """
        A method for getting unique records from response dataframe by comparing with database.
        :param response_df:
        :return: A dataframe with unique ip_address records
        """
        ip_table = conf.read().get('db-conf', 'ip_table')
        try:
            table = pd.read_sql("SELECT * FROM {};".format(ip_table), con=self.db.engine, chunksize=self.chunk_size)
            while True:
                chunk = next(table)
                response_df = response_df[~response_df['ip_address'].isin(chunk['ip_address'].values)]
                if len(chunk.index) < self.chunk_size:
                    break
            return response_df
        except (StopIteration, TypeError) as err:
            logger.exception(err, exc_info=False)

    @staticmethod
    def get_loc_updates(dataset):
        """
        A method for getting location updates for country, city, latitude, longitude for given dataframe.
        :param dataset: pandas dataframe with column country city latitude and longitude
        :return: updated pandas DataFrame
        """
        df = dataset
        unknown_country = df.index[df['country'].isin(['unknown'])].tolist()
        unknown_cities = df.index[df['city'].isin(['unknown'])].tolist()
        zero_lat = df.index[df['latitude'].isin(['0'])].tolist()
        zero_long = df.index[df['longitude'].isin(['0'])].tolist()
        try:
            if len(unknown_country) > 0:
                for i in unknown_country:
                    ip = df.at[i, 'ip_address']
                    country = LocationUpdater(ip).get_country()
                    if country is not None:
                        country.encode('utf-8')
                        df.at[i, 'country'] = country
            if len(unknown_cities) > 0:
                for i in unknown_cities:
                    ip = df.at[i, 'ip_address']
                    city = LocationUpdater(ip).get_city()
                    if city is not None:
                        city.encode('utf-8')
                        df.at[i, 'city'] = city
            if len(zero_lat) > 0:
                for i in zero_lat:
                    ip = df.at[i, 'ip_address']
                    lat = LocationUpdater(ip).get_latitude()
                    if lat is not None:
                        df.at[i, 'latitude'] = lat
            if len(zero_long) > 0:
                for i in zero_long:
                    ip = df.at[i, 'ip_address']
                    long = LocationUpdater(ip).get_longitude()
                    if long is not None:
                        df.at[i, 'longitude'] = long
        except AddressNotFoundError as err:
            logger.exception(err, exc_info=False)
        return df

    @staticmethod
    def diff_df(df1, df2, how="left"):
        """
        Find Difference of rows for given two dataframe
        :param df1: pandas DataFrame
        :param df2: pandas DataFrame
        :param how: left or right in string
        :return: Difference DataFrame
        """
        if (df1.columns != df2.columns).any():
            raise ValueError("Two dataframe columns must match")
        if df1.equals(df2):
            return None
        elif how == 'right':
            return pd.concat([df2, df1, df1]).drop_duplicates(keep=False)
        elif how == 'left':
            return pd.concat([df1, df2, df2]).drop_duplicates(keep=False)
        else:
            raise ValueError('how parameter supports only "left" or "right keywords"')

    def get_difference(self, response_df):
        """
        A method for getting changed cell values of existing records against database records
        :param response_df: A dataframe generated from response
        :return: None
        """
        ip_table = conf.read().get('db-conf', 'ip_table')
        try:
            table = pd.read_sql(
                "SELECT * FROM {};".format(ip_table), con=self.db.engine, chunksize=self.chunk_size
            )
            cols = [
                'ip_address', 'reliability', 'priority', 'activity', 'sub_category', 'country', 'city', 'latitude',
                'longitude', 'source', 'target', 'dest_port', 'last_online', 'first_seen', 'used_by', 'reference_link'
            ]
            df = response_df
            diff_df = []
            while True:
                chunk = next(table)
                exist_df = df[df['ip_address'].isin(chunk['ip_address'].values)]
                exist_df = exist_df.sort_values('ip_address').reset_index(drop=True)
                chunk_df = chunk[chunk['ip_address'].isin(exist_df['ip_address'].values)]
                chunk_df = chunk_df.sort_values('ip_address').reset_index(drop=True)
                chunk_df = chunk_df[cols]
                exist_df = exist_df[cols]
                diff = self.diff_df(exist_df, chunk_df, how='left')
                diff_df.append(diff)
                if len(chunk.index) < self.chunk_size:
                    break
            self._updated_df = pd.concat(diff_df)
            return self._updated_df
        except (StopIteration, TypeError, ValueError) as err:
            logger.exception(err, exc_info=False)
