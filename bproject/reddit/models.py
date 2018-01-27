from django.db import models


class Submission(models.Model):
    title = models.CharField(max_length=200)
    external_url = models.URLField(max_length=200)
    discussion_url = models.URLField(max_length=200)
    submitter = models.CharField(max_length=200)
    punctuation = models.IntegerField(default=0)
    creation_date = models.DateTimeField()
    number_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} by {self.submitter}'
