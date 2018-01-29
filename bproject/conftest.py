import time
import pytest

TIMESTAMP = time.time()


@pytest.fixture()
def praw_submission(mocker):
    sub_mock = mocker.Mock(
        title='foo',
        url='https://url.com',
        permalink='/r/python/',
        author='foo',
        score=1,
        created_utc=TIMESTAMP,
        comments=['abc', ]
    )
    return sub_mock
