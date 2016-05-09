#! /usr/bin/env python

# import and setup Django environment (as "./manage.py shell" does):
from sys import argv, path as sys_path
import os
import django

sys_path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")
django.setup()

# actual import script:
from persons.models import Person
from jobs.models import Job
from random import choice

if __name__ == '__main__':
    if len(argv) != 2:
        print('USAGE: $ ./import.py /some/path/file.txt')
    else:
        imported_persons_count = 0
        with open(argv[1], 'r') as input_file:
            for line in input_file:
                short, full, mail = line.split('\t')
                person = Person(short_name=short, full_name=full, email=mail)
                #person.job = choice(Job.objects.all())
                person.update_jobs()
                print(person)
                #print(person.job.description)
                person.save()  # write new row to DB

                imported_persons_count += 1
        print('Imported %s persons.' % imported_persons_count)