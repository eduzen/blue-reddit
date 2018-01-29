import pytest
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from reddit.views import SubmissionViewSet
from reddit.models import Submission


@pytest.fixture()
def submissions():
    s = [
        Submission(
            title=f'foo{x}',
            external_url=f'https://url{x}.com',
            discussion_url=f'/r/python/{x}',
            submitter='foo',
            punctuation=x,
            creation_date=timezone.now(),
            number_of_comments=x
        )
        for x in range(10)
    ]

    subs = Submission.objects.bulk_create(s)
    return subs


@pytest.fixture()
def submissions_15():
    s = [
        Submission(
            title=f'foo{x}',
            external_url=f'https://url{x}.com',
            discussion_url=f'/r/python/{x}',
            submitter='foo',
            punctuation=x,
            creation_date=timezone.now(),
            number_of_comments=x
        )
        for x in range(14)
    ]

    subs = Submission.objects.bulk_create(s)
    return subs


@pytest.mark.django_db
def test_get_submission(rf, submissions):
    request = rf.get('/submission/')
    submission_view = SubmissionViewSet.as_view({'get': 'list'})
    response = submission_view(request)
    results = [
        r.get('title')
        for r in response.data.get('results')
    ]

    expected = [
        r.title
        for r in submissions
    ]

    assert response.status_code == 200
    assert expected == results


@pytest.mark.django_db
def test_get_submission_paginated(rf, submissions_15):
    request = rf.get('/submission/')
    submission_view = SubmissionViewSet.as_view({'get': 'list'})
    response = submission_view(request)

    assert response.status_code == 200
    assert len(response.data.get('results')) == 10
