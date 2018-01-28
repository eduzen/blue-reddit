from __future__ import absolute_import, unicode_literals

import praw
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings

from .models import Submission

logger = get_task_logger(__name__)


@task(name="collect_submissions")
def collect_submissions():

    reddit = praw.Reddit(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        user_agent=settings.USER_AGENT,
        username=settings.USERNAME,
        password=settings.PASSWORD,
    )
    for submission in reddit.subreddit('python').hot(limit=10):
        submission = Submission.objects.create(
            title=submission.title,
            submitter=submission.author,
            punctuation=submission.score,
            creation_date=submission.created_utc,
        )
