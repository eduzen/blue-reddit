import pytest
from rest_framework.test import APIRequestFactory

from reddit.views import SubmissionViewSet


@pytest.mark.django_db
def test_get_all_submission():
    factory = APIRequestFactory()
    request = factory.post('/submission/', {'title': 'new idea'})

    submission_view = SubmissionViewSet.as_view({'post': 'list'})
    response = submission_view(request)

    assert response.status_code == 200
