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
