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
from urls.processor import Processor
from common.crawler import Crawler


class URLDriver:
    """
    A class for gathering logic for main function
    """
    def __init__(self):
        self.process = Processor(chunk_size=30000)
        self.crawl = Crawler()
        self.logger = logger

    def first_run(self, dataset, url):
        """
        A logic to run only for the first time
        :param dataset: response dataframe
        :param url: http url endpoint
        :return: None
        """
        log = self.logger
        try:
            if 'ransomware' in url:
                log.info("Found ransomware url")
                ransom = self.process.handle_ransomware(dataset=dataset)
                log.info("Database insert started")
                self.process.insert_db(dataset=ransom)
                log.info("{} records inserted into database successfully".format(len(dataset)))
                log.info("Removing duplicates")
                self.process.db.url_remove_duplicates()
            else:
                updated = self.process.get_url_updates(dataset=dataset)
                log.info("Database insert started")
                self.process.insert_db(dataset=updated)
                log.info("{} records inserted into database successfully".format(len(dataset)))
                log.info("Removing duplicates")
                self.process.db.url_remove_duplicates()
        except Exception as err:
            self.logger.exception(err, exc_info=False)

    def normal_run(self, dataset, url):
        """
        A logic to run regularly
        :param dataset: response dataframe
        :param url:
        :return: None
        """
        log = self.logger
        try:
            if 'ransomware' in url:
                log.info("Found ransomware url")
                if not dataset:
                    log.info("{} records found".format(len(dataset)))
                    log.info("Applying domain, filename, file_type and threat_type to the records")
                    updated = self.process.get_url_updates(dataset=dataset)
                    ransom = self.process.handle_ransomware(dataset=updated)
                    log.info("Database insert started")
                    log.info("Querying database")
                    self.process.insert_db(dataset=ransom)
                    log.info("Records inserted into database successfully")
                else:
                    log.info("No unique records found")
            else:
                if not dataset.empty:
                    log.info("{} records found".format(len(dataset)))
                    log.info("Applying domain, filename, file_type and threat_type to the records")
                    updated = self.process.get_url_updates(dataset=dataset)
                    log.info("Database insert started")
                    log.info("Querying database")
                    self.process.insert_db(dataset=updated)
                    log.info("Records inserted into database successfully")
                else:
                    log.info("No unique records found")
        except Exception as err:
            logger.exception(err, exc_info=False)

    def url_main(self):
        """
        Main driver code for running operation with all urls
        :return: None
        """
        log = self.logger
        st = time.time()
        print("Running...\nCheck logs/threat_hub.log for detailed events")
        log.info("URL Threat intell hub started")
        log.info("database cleanup started")
        self.process.flush_db()
        log.info("database flushed successfully")
        try:
            for url in self.crawl.url_targets:
                response = self.crawl.send_request(url=url)
                if not response:
                    continue
                else:
                    dataset = self.process.shape_up(raw_data=response)
                    # self.first_run(dataset, url)
                    self.normal_run(dataset, url)
            log.info(f"Total {self.process.db.get_total_url()} url records present.")
            log.info(f"Total {self.process.db.get_phishing_count()} phishing urls present")
            log.info(f"Total {self.process.db.get_malware_count()} malware urls present")
            log.info(f"Total {self.process.db.get_ransom_count()} ransomware urls present")

        except Exception as err:
            log.exception(err, exc_info=False)
        finally:
            end = time.time()
            log.info("Finished executing threat intell hub in {} seconds".format(end - st))
            print("Finished...")


if __name__ == '__main__':
    URLDriver().url_main()
