# -*- coding: utf-8 -*-
"""
Utility functions for main module
Created on 10/9/2019
@author: Anurag
"""
# imports
import time

# Local imports
from common.logger import logger
from common.crawler import Crawler
from ip_address.processor import Processor


class IPDriver:
    """
    A class for gathering logic for main function
    """
    def __init__(self):
        """
        Constructor
        """
        self.process = Processor(chunk_size=30000)
        self.crawl = Crawler()
        self.logger = logger

    def first_run(self, dataset):
        """
        A logic to run only for the first time
        :param dataset: response dataframe
        :return: None
        """
        log = self.logger
        try:
            log.info("Database insert started")
            self.process.insert_db(dataset=dataset)
            log.info("Records inserted into database successfully")
            log.info("Removing duplicates")
            self.process.db.ip_remove_duplicates()
        except Exception as err:
            log.exception(err, exc_info=False)

    def normal_run(self, dataset):
        """
        A logic to run regularly
        :param dataset: response dataframe
        :return: None
        """
        log = self.logger

        ####
        try:
            uniq = self.process.get_unique(response_df=dataset)
        except Exception as err:
            log.exception(err)
        ####

        try:
            if not dataset.empty:
                log.info("Database insert started")
                log.info("Applying location data to the ip records")
                self.process.get_loc_updates(dataset)
                log.info("Querying database")
                self.process.insert_db(dataset)
                log.info("Records inserted into database successfully")
                log.info("Removing duplicates")
                self.process.db.ip_remove_duplicates()
            else:
                log.info("No unique records found")
        except Exception as err:
            log.exception(err, exc_info=False)

    def ip_main(self):
        """
        Main driver code for running operation with all urls
        :return: None
        """
        log = self.logger
        st = time.time()
        print("Started...\nCheck logs/threat_hub.log for detailed events")
        log.info("IP Threat intell hub started")
        log.info("database cleanup started")
        self.process.flush_db()
        log.info("database flushed successfully")
        try:
            check = 0
            current_rev = self.process.revision.current_revision
            if not current_rev:
                log.info("first start detected, creating initial revision")
                self.process.db.write_first_revision_for_tracker()
            for url in self.crawl.ip_targets:
                response = self.crawl.send_request(url=url)
                if not response:
                    check += 1
                    continue
                else:
                    dataset = self.process.shape_up(raw_data=response)
                    # self.first_run(dataset)
                    self.normal_run(dataset)
            if not check >= self.crawl.total_urls:
                self.process.revision.update_revision_to_db()
        except Exception as err:
            log.exception(err, exc_info=False)
        finally:
            log.info(f"Total {self.process.db.get_total_ip()} ip-address present.")
            end = time.time()
            log.info("Finished executing threat intell hub in {} seconds".format(end - st))
            print("Finished...")


if __name__ == '__main__':
    IPDriver().ip_main()
