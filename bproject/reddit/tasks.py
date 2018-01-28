from __future__ import absolute_import, unicode_literals

import pytz
from datetime import datetime

import praw
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings

from .models import Submission

logger = get_task_logger(__name__)


def _update_or_create_submission(submission_data):
    """
        It creates a new row in the database from submission data or if it
        doesn't exist, we update it.

        Args:
            submission_data (praw.submission): data from praw api.
    """
    obj, created = Submission.objects.update_or_create(
        title=submission_data.title,
        submitter=submission_data.author,
        discussion_url=submission_data.permalink,
        external_url=submission_data.url,
        creation_date=datetime.fromtimestamp(
            submission_data.created_utc, tz=pytz.UTC),
        defaults={
            'punctuation': submission_data.score,
            'number_of_comments': len(submission_data.comments),
        },
    )
    if created:
        logger.info(f'New submission, created! Id: {obj.id}')
    else:
        logger.info(f'Updated submission, created! Id: {obj.id}')


def _create_submission(submission_data):
    """
        It only creates in memory a new submission.
        Args:
            submission_data (praw.submission): data from praw api.
    """
    submission = Submission(
        title=submission_data.title,
        submitter=submission_data.author,
        punctuation=submission_data.score,
        creation_date=submission_data.created_utc,
        number_of_comments=len(submission_data.comments),
        discussion_url=submission_data.permalink,
        external_url=submission_data.url,
    )
    return submission


def _save_submissions(submissions):
    """
        It saves a list of submissions in the database.

        Args:
            list_of_submissions (list): a list of submissions
    """
    Submission.objects.bulk_create(submissions)


def _reddit_connection():
    reddit = praw.Reddit(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        user_agent=settings.USER_AGENT,
        username=settings.USERNAME,
        password=settings.PASSWORD,
    )
    return reddit


@task(name="collect_submissions")
def collect_submissions(limit=15):
    """
        It gathers the newst submissions from reddit and it persists them
        into the database.

        Args:
            limit (int): a number of submissions
    """
    try:
        reddit = _reddit_connection()
    except Exception:
        logger.Exception()

    for submission in reddit.subreddit('python').new(limit=limit):
        try:
            _update_or_create_submission(submission)
        except Exception:
            logger.exception("We could not create a new submission")
