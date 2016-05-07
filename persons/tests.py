from django.test import TestCase
from django.test.client import Client
from persons.models import Person as P

class PersonTestCase(TestCase):
    def setUp(self):
        P.objects.create(short_name='mwon', full_name='Michael Won')
        P.objects.create(short_name='jim12', full_name='James D. Costning',
                                email='jim12@jimbo.people.we.com')
        P.objects.create(short_name='world_master')

    def test_persons_count(self):
        self.assertEqual(P.objects.count(), 3)

    def test_persons_fields(self):
        persons = P.objects.all()
        correct_values = {
            'mwon' : {'str' : 'mwon (Michael Won)', 'email' : None},
            'jim12' : {'str' : 'jim12 (James D. Costning)',
                                'email' : 'jim12@jimbo.people.we.com'},
            'world_master' : {'str' : 'world_master', 'email' : None},
        }

        for p in persons:
            vals = correct_values[p.short_name]
            self.assertEqual(str(p), vals['str'])
            self.assertEqual(p.email, vals['email'])
