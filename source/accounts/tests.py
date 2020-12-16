from django.test import TestCase

from django.contrib.auth import get_user_model, authenticate


class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='islam')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_wrong_username(self):
        user = authenticate(username='islamm', password='islam')
        print(user)
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='islam', password='islam')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_success_login(self):
        user = authenticate(username='test', password='islam')
        self.assertTrue(user is not None and user.is_authenticated)
