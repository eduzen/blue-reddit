import pytest
from django.utils import timezone

from reddit.models import Submission


@pytest.mark.django_db
def test_save():
    sub = Submission(
        title="Test",
        external_url="http://www.reddit.com",
        discussion_url='/r/python/',
        submitter='Edu',
        punctuation=1,
        creation_date=timezone.now(),
        number_of_comments=1
    )
    sub.save()
    assert sub.title == "Test"
    assert sub.submitter == "Edu"


@pytest.mark.parametrize("url, expected", [
    ("http://www.reddit.com", None),
    ("http://redd.it", None),
    ("http://eduzen.com.ar/util", 'http://eduzen.com.ar/util'),
    ("http://www.github.com:80/foo/bar",
     "http://www.github.com:80/foo/bar"),
])
@pytest.mark.django_db
def test_save_non_external_url(url, expected):
    sub = Submission(
        title="Test",
        external_url=url,
        discussion_url='/r/python/',
        submitter='Edu',
        punctuation=1,
        creation_date=timezone.now(),
        number_of_comments=1
    )
    sub.save()
    assert sub.external_url == expected


@pytest.mark.parametrize("url", [
    "/r/python/asdab", "r/redd",
    '/r/Python/comments/7tknzf/python_advice/',
])
@pytest.mark.django_db
def test_save_discuss_url(url):
    sub = Submission(
        title="Test",
        external_url=url,
        discussion_url='/r/python/',
        submitter='Edu',
        punctuation=1,
        creation_date=timezone.now(),
        number_of_comments=1
    )
    sub.save()
    assert "https://www.reddit.com" in sub.discussion_url
