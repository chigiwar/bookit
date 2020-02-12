from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from account.models import User
from .api import views


class TestBook(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.BookViewSet.as_view({'get': 'list'})
        self.uri = '/api/v1/booking/books'
        self.user = self.setup_user()

    @staticmethod
    def setup_user():

        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test',
            group='admin',
            vip=True
        )

    def test_unauthorised(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 401,
                         'Expected Response Code 401, received {0} instead.'
                         .format(response.status_code))

    def test_list(self):
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
