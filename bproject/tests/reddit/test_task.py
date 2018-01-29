import time
import pytz
from datetime import datetime

import pytest

from conftest import TIMESTAMP
from reddit.models import Submission
from reddit.tasks import (
    _update_or_create_submission,
    _create_submission,
    _save_submissions,
    collect_submissions,
)


@pytest.fixture()
@pytest.mark.django_db
def sub():
    subs = Submission.objects.create(
        title='foo',
        external_url='https://url.com',
        discussion_url='/r/python/',
        submitter='foo',
        punctuation=1,
        creation_date=datetime.fromtimestamp(TIMESTAMP, tz=pytz.UTC),
        number_of_comments=3
    )
    return subs


def test_collect_submissions_fail_connection(mocker):
    mocked_reddit = mocker.patch(
        'reddit.tasks._reddit_connection', side_effect=Exception())

    with pytest.raises(Exception):
        collect_submissions()

    assert mocked_reddit.called


def test_collect_submissions_connected_non_submissions(mocker):
    reddit_connection = mocker.MagicMock()
    reddit_connection.subreddit.new = []
    mocked_reddit = mocker.patch('reddit.tasks._reddit_connection')
    mocked_reddit.side_effect = reddit_connection

    mocked_update_or_create = mocker.patch(
        'reddit.tasks._update_or_create_submission')

    collect_submissions()

    assert mocked_reddit.called
    assert not mocked_update_or_create.called


@pytest.mark.django_db
def test_update_or_create_submission_update(sub, praw_submission):
    created = _update_or_create_submission(praw_submission)
    assert not created


@pytest.mark.django_db
def test_update_or_create_submission_update_log(sub, praw_submission, mocker):
    mocked_log = mocker.patch('reddit.tasks.logger.info')
    _update_or_create_submission(praw_submission)

    assert mocked_log.called


@pytest.mark.django_db
def test_update_or_create_submission_create(sub, praw_submission):
    praw_submission.created_utc = time.time()
    created = _update_or_create_submission(praw_submission)
    assert created


@pytest.mark.django_db
def test_update_or_create_submission_create_log(sub, praw_submission, mocker):
    praw_submission.created_utc = time.time()
    mocked_log = mocker.patch('reddit.tasks.logger.info')
    _update_or_create_submission(praw_submission)

    assert mocked_log.called


@pytest.mark.django_db
def test_create_submission(praw_submission):
    submission = _create_submission(praw_submission)
    assert submission


@pytest.mark.django_db
def test_save_submissions(sub, mocker):
    mocked_bulk = mocker.patch('reddit.tasks.Submission.objects.bulk_create')
    _save_submissions([sub, ])
    assert mocked_bulk.called
