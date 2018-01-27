# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'external_url',
        'discussion_url',
        'submitter',
        'punctuation',
        'creation_date',
        'number_of_comments',
    )
    list_filter = ('creation_date',)
