# -*- coding: utf-8 -*-
"""
Ip address location updater using local db on given parameters
Created on 10/9/2019
@author: Anurag
"""

# imports
import time
import datetime

# local imports
from api.models import RevisionTrackerModel, db
from manage import create_app

app = create_app()
app.app_context().push()


class RevisionTracker:
    """
    A class for tracking and managing database upgrade version
    """

    def __init__(self):
        """
        Constructor
        """
        self._current_revision = None
        self._last_revision = None

    @property
    def current_revision(self):
        """
        A getter for getting current revision number present in db
        :return:
        """
        revision = RevisionTrackerModel.query.all()
        if not len(revision) > 0:
            return 0
        return revision[0].last_revision

    def update_revision_to_db(self):
        """
        A method for updating revision number in database
        :return:
        """
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        record_id = int(RevisionTrackerModel.query.first().id)
        RevisionTrackerModel.query.filter_by(id=record_id).update(dict(
            last_revision=self.current_revision + 1,
            updated_at=timestamp
        ))
        db.session.commit()
