from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Submission
from .serializers import SubmissionSerializer
from .tasks import collect_submissions


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SubmissionViewSet(ModelViewSet):
    """
        This viewset automatically provides `list` and `create` actions for
        Submision.

        You can filter, search and order this previous
        results. For instance:
          `submission?search=github
         This will search Submission with external url and it contains github
        inside of this field.

    """

    serializer_class = SubmissionSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Submission.objects.all()
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('punctuation', 'creation_date', 'number_of_comments')
    search_fields = ('external_url', )
    ordering_fields = ('punctuation', 'creation_date', 'number_of_comments')


class SubmissionsUrlListView(ListAPIView):
    """
        This viewset `list` the submissions filter by an external or
        internal url.
          - /submission/internal`: will give you non external url
          - `/submission/external`: will give you external url

        On the other hand you can filter and order this previous
        results. For instance:
          `- submission/internal?number_of_comments>0&punctuation>1&ordering=punctuation`  # noqa
        This will return non external url, number of coments greater than 0,
        punctuation greater than 1 and order by punctuation

    """
    serializer_class = SubmissionSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Submission.objects.all()
    filter_backends = (
        DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('punctuation', 'creation_date', 'number_of_comments')
    ordering_fields = ('punctuation', 'creation_date', 'number_of_comments')

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        url = self.kwargs['url']
        if 'external' in url:
            return self.queryset.exclude(external_url__isnull=True)
        elif 'interal':
            return self.queryset.exclude(external_url__isnull=False)


class CollectSubmissionsView(APIView):
    """
        This view helps you to collect automatically submission from Reddit
        and it avoids to create submissions already existing.
    """
    json_response = {
        "message": "We will start to gather new submissions. Task created!"
    }

    def post(self, request, format=None):
        limit = self.request.query_params.get('limit', None)
        if not limit:
            collect_submissions.delay()
            return Response(self.json_response, status=status.HTTP_201_CREATED)

        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {'message': 'Limit must be a integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        collect_submissions.delay(limit)
        return Response(self.json_response, status=status.HTTP_201_CREATED)
