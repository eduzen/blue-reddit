from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Submission
from .serializers import SubmissionSerializer
from .tasks import collect_submissions


class SubmissionViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class CollectSubmissions(APIView):
    """
    View to collect submission from Reddit
    """

    def post(self, request, format=None):
        json_response = {
            "message": "We will start to gather new submissions. Task created!"
        }
        collect_submissions.delay()
        return Response(json_response, status=status.HTTP_201_CREATED)
