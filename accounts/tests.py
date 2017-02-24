from django.test import TestCase
from django.test import Client
import django.contrib.auth as auth


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        c = Client()
        response = c.post('/accounts/register/', {'username': 'john',
                                        'password1': 'smith',
                                        'password2': 'smith',
                                        'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        user = auth.models.User.objects.get_by_natural_key('john')
        self.assertTrue(user is not None)

    def test_login(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 'john',
                                      'password': 'smith'})
        self.assertEqual(response.status_code, 302)
