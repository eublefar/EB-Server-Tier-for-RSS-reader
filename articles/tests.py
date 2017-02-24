from django.test import TestCase
from django.test import Client
import django.contrib.auth as auth
from models import Source,User_source
# Create your tests here.
class SourceAddDelete(TestCase):
    def setUp(self):
        c = Client()
        response = c.post('/accounts/register/', {'username': 'john',
                                        'password1': 'smith',
                                        'password2': 'smith',
                                        'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        user = auth.models.User.objects.get_by_natural_key('john')
        self.assertTrue(user is not None)

    def test_add(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 'john',
                                      'password': 'smith'})
        self.assertEqual(response.status_code, 302)
        response = c.post('/articles/sources/', {'source_address':'www.exampl.com', 'source_name':'example'})
        self.assertEqual(response.status_code, 200)
        source = Source.objects.filter(source_name='example')
        self.assertNotEqual(len(source), 0)
        user = auth.models.User.objects.get_by_natural_key('john')
        relation = User_source.objects.filter(user=user, source=source[0])
        self.assertNotEqual(len(relation), 0)

    def test_delete(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 'john',
                                      'password': 'smith'})
        self.assertEqual(response.status_code, 302)
        response = c.post('/articles/sources/', {'source_address':'www.exampl.com', 'source_name':'example'})
        self.assertEqual(response.status_code, 200)

        response = c.delete('/articles/sources/', {'source_address':'www.exampl.com'})
        self.assertEqual(response.status_code, 200)
        source = Source.objects.filter(source_name='example')
        self.assertEqual(len(source), 0)
        user = auth.models.User.objects.get_by_natural_key('john')
        relation = User_source.objects.filter(user=user)
        self.assertEqual(len(relation), 0)
