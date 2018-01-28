from django.conf.urls import url, include
from django.urls import path

from rest_framework.documentation import include_docs_urls
from rest_framework import routers

from .views import (
    SubmissionViewSet, CollectSubmissionsView, SubmissionsUrlListView,
)

router = routers.DefaultRouter()
router.register(r'^submission', SubmissionViewSet)

urlpatterns = [
    path(
        'collect-submissions',
        CollectSubmissionsView.as_view(),
        name='collect-submissions'
    ),
    path(
        'submission/<str:url>',
        SubmissionsUrlListView.as_view(),
        name='external_url_submissions',
    ),
    path('', include(router.urls)),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    path('docs/', include_docs_urls(title='My Reddit crawler'))
]
