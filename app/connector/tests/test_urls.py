from django.test import SimpleTestCase
from django.urls import resolve, reverse

from connector import views


class UrlsTest(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('api_login')
        self.assertEqual(resolve(url).func.view_class, views.UserLoginView)

    def test_registration_url_resolves(self):
        url = reverse('api_register')
        self.assertEqual(
            resolve(url).func.view_class, views.UserRegistrationView
        )

    def test_verify_otp_url_resolves(self):
        url = reverse('api_verification')
        resolver_match = resolve(url)
        self.assertEqual(
            resolver_match.func.cls, views.EmailVerificationViewSet
        )
        self.assertEqual(resolver_match.func.actions['post'], 'verify_otp')

    def test_user_url_retrieve_resolves(self):
        url = reverse('user')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.cls, views.UserViewSet)
        self.assertEqual(resolver_match.func.actions['get'], 'retrieve')

    def test_user_url_delete_resolves(self):
        url = reverse('user')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.cls, views.UserViewSet)
        self.assertEqual(resolver_match.func.actions['delete'], 'delete')

    def test_user_url_update_resolves(self):
        url = reverse('user')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.cls, views.UserViewSet)
        self.assertEqual(resolver_match.func.actions['put'], 'update')
