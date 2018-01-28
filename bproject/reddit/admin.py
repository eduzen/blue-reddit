# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'submitter',
        'punctuation',
        'creation_date',
        'number_of_comments',
        'discussion_url',
        'external_url',
    )
    list_filter = ('creation_date', 'submitter')
