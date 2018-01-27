from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            'title', 'external_url', 'discussion_url', 'submitter',
            'punctuation', 'creation_date', 'number_of_comments'
        )
