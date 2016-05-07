# -*- coding: utf-8 -*-
import os
import django
from sys import path as sys_path  ###
import json
import urllib.request
sys_path.append('..')                   ###
URL_WITH_JSON = 'http://standards.openprocurement.org/classifiers/dk003/uk.json'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")
django.setup()
from jobs.models import Job


if __name__ == '__main__':
    imported_jobs_count = 0
    with urllib.request.urlopen(URL_WITH_JSON) as json_file:
        dict_from_json = json.loads(json_file.read().decode('utf-8'))
#        print(dict)
    for key in dict_from_json.keys():
        code = key
        descr = dict_from_json.get(key)
        job = Job(code_job=code, description=descr)
        job.save()
        imported_jobs_count += 1
        print(code, descr)
    print('Imported %s jobs.' % imported_jobs_count)
