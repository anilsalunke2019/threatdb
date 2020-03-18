# -*- coding: utf-8 -*-
"""
A central processor for database insert / update logic
Created on 10/9/2019
@author: Anurag
"""

# imports
import time
import datetime
import pandas as pd

# local imports
from common.logger import logger
from common.threat_orm import ThreatDB
from common.config import conf
from urls.parser import URLParser
from api.views import MalwareURLsModel
from api.models import db
from manage import create_app

app = create_app()
app.app_context().push()


class Processor:
    """
    A class for processing input data and for inserting / updating the database
    """

    def __init__(self, chunk_size=None):
        self._dataset = pd.DataFrame()
        self._updated_df = pd.DataFrame()
        self.chunk_size = chunk_size
        self.db = ThreatDB()

    def shape_up(self, raw_data):
        """
        A method for preparing pandas self.dataset from raw JSON
        :param raw_data: A input JSON data from URL response.
        :return: Pandas self.dataset
        """
        dataset = self._dataset.from_dict(raw_data, orient='index')
        dataset.reset_index(level=0, inplace=True)
        dataset.rename(columns={
            'index': 'url',
        }, inplace=True)
        dataset.drop_duplicates(subset='url', keep='first', inplace=True)
        cols = [
            'url', 'domain', 'filename', 'file_type', 'priority', 'country',
            'url_status', 'date_added', 'threat_type', 'threat_tag'
        ]
        dataset = dataset[cols].astype('str')
        return dataset

    def insert_db(self, dataset):
        """
        A method to insert pandas dataframe into database
        :return: None
        """
        url = dataset['url'].values
        domain = dataset['domain'].values
        filename = dataset['filename'].values
        file_type = dataset['file_type'].values
        priority = dataset['priority'].values
        country = dataset['country'].values
        url_status = dataset['url_status'].values
        date_added = dataset['date_added'].values
        threat_type = dataset['threat_type'].values
        threat_tag = dataset['threat_tag'].values
        for i in range(len(dataset)):
            try:
                record = MalwareURLsModel(
                    url=str(url[i]),
                    domain=str(domain[i]),
                    filename=str(filename[i]),
                    file_type=str(file_type[i]),
                    priority=str(priority[i]),
                    country=str(country[i]),
                    url_status=str(url_status[i]),
                    date_added=str(date_added[i]),
                    threat_type=str(threat_type[i]),
                    threat_tag=str(threat_tag[i]),
                )
                db.session.add(record)
                db.session.commit()
            except Exception:
                db.session.rollback()

    @staticmethod
    def get_url_updates(dataset):
        """
        Method for adding domain, filename, file_type and threat type to URLs
        :param dataset:
        :return: updated dataFrame
        """
        df = dataset
        indices = list(df.index)
        for i in indices:
            url = df.at[i, 'url']
            parser = URLParser(url)
            domain = parser.get_domain()
            file_name = parser.get_filename()
            file_type = parser.get_filetype()
            threat = parser.get_threat_type()
            df.at[i, 'domain'] = domain
            df.at[i, 'filename'] = file_name
            df.at[i, 'file_type'] = file_type
            df.at[i, 'threat_type'] = threat
        return df

    @staticmethod
    def handle_ransomware(dataset):
        """
        A method to return dataset with setting threat_type column to 'ransomware'
        :param dataset:
        :return:
        """
        dataset['threat_type'] = 'ransomware'
        return dataset

    @staticmethod
    def flush_db():
        """
        A method to clean the malware_url table
        """
        try:
            MalwareURLsModel.query.delete()
            db.session.commit()
        except Exception as err:
            print(err)

    def commit_changes(self, dataset):
        """
        A method for actually commiting changes to the database
        :param dataset: difference dataFrame
        :return: None
        """
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        url = dataset['url'].values
        domain = dataset['domain'].values
        filename = dataset['filename'].values
        file_type = dataset['file_type'].values
        priority = dataset['priority'].values
        country = dataset['country'].values
        url_status = dataset['url_status'].values
        date_added = dataset['date_added'].values
        threat_type = dataset['threat_type'].values
        threat_tag = dataset['threat_tag'].values
        for i in range(len(dataset)):
            MalwareURLsModel.query.filter_by(url=str(url[i])).update(dict(
                domain=str(domain[i]),
                filename=str(filename[i]),
                file_type=str(file_type[i]),
                priority=str(priority[i]),
                country=str(country[i]),
                url_status=str(url_status[i]),
                date_added=str(date_added[i]),
                threat_type=str(threat_type[i]),
                threat_tag=str(threat_tag[i]),
                updated_at=timestamp,
                ))

    def get_unique(self, response_df):
        """
        A method for getting unique records from response dataframe by comparing with database.
        :param response_df:
        :return: A dataframe with unique ip_address records
        """
        url_table = conf.read().get('db-conf', 'url_table')
        try:
            table = pd.read_sql_query(
                sql="SELECT * FROM {};".format(url_table), con=self.db.engine, chunksize=self.chunk_size
            )
            while True:
                chunk = next(table)
                response_df = response_df[~response_df['url'].isin(chunk['url'].values)]
                if len(chunk.index) < self.chunk_size:
                    break
            return response_df
        except (StopIteration, TypeError) as err:
            logger.exception(err, exc_info=False)

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
        try:
            table = pd.read_sql(
                "SELECT * FROM {};".format(urls_db['table_name']), con=self.db.engine, chunksize=self.chunk_size
            )
            cols = [
                'url', 'domain', 'filename', 'file_type', 'priority', 'country', 'url_status', 'date_added',
                'threat_type', 'threat_tag',
            ]
            df = response_df
            diff_df = []
            while True:
                chunk = next(table)
                exist_df = df[df['url'].isin(chunk['url'].values)]
                exist_df = exist_df.sort_values('url').reset_index(drop=True)
                chunk_df = chunk[chunk['url'].isin(exist_df['url'].values)]
                chunk_df = chunk_df.sort_values('url').reset_index(drop=True)
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
