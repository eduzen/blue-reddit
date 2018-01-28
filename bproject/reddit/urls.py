from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers

from .views import SubmissionViewSet, CollectSubmissions

router = routers.DefaultRouter()
router.register(r'submission', SubmissionViewSet)

urlpatterns = [
    path(
        'collect-submissions',
        CollectSubmissions.as_view(),
        name='collect-submissions'
    ),
    url(r'^', include(router.urls)),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
]
