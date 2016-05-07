from django.db import models


class Job(models.Model):
    code_job = models.IntegerField
    description = models.CharField(max_length=128, null=True, blank=True)


class FilteredJobsWrapper(models.Model):
    def __init__(self, code_digit_sum):
        return None