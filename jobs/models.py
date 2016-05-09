from django.db import models
#from persons.models import Person


class Job(models.Model):
    code_job = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    def code_sum(self):
        for i in self.code_job.replace('.', ''):
            sum += int(i)
        return sum


class FilteredJobsWrapper:
    def __init__(self, code_digit_sum):
        if 4 < code_digit_sum < 16:
            self.sum = code_digit_sum
            self.all = len(Job.objects.all())
            self.current = 1                  # try 0

    def __iter__(self):
        if Job.code_sum == self.sum:
            return Job

    def __next__(self):
        if self.current > self.all:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

