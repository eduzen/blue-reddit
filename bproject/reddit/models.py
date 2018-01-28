from urllib.parse import urlparse

from django.db import models


class Submission(models.Model):
    title = models.CharField(max_length=200)
    external_url = models.URLField(max_length=200, null=True, blank=True)
    discussion_url = models.URLField(max_length=200)
    submitter = models.CharField(max_length=200)
    punctuation = models.IntegerField(default=0)
    creation_date = models.DateTimeField()
    number_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} by {self.submitter}'

    @property
    def outside_link(self):
        url = urlparse(self.external_url)
        if 'reddit.com' not in url.netloc or 'redd.it' not in url.netloc:
            return True

        return False

    def save(self, *args, **kwargs):
        if not self.outside_link:
            self.external_url = None

        self.discussion_url = f"https://www.reddit.com{self.discussion_url}"
        return super(Submission, self).save(*args, **kwargs)

    class Meta:
        ordering = ('creation_date', 'punctuation', 'number_of_comments')
