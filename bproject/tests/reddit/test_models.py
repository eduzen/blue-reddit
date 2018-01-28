import pytest
from django.utils import timezone

from reddit.models import Submission


@pytest.mark.django_db
def test_save():
    sub = Submission(
        title="Test",
        external_url="www.reddit.com",
        discussion_url='/r/python/',
        submitter='Edu',
        punctuation=1,
        creation_date=timezone.now(),
        number_of_comments=1
    )
    sub.save()
    assert sub.title == "Test"
    assert sub.submitter == "Edu"
