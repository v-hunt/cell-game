from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.urls.exceptions import NoReverseMatch

from base.tests.factories import John, ActiveUser
from my_game.gamer import Gamer


class GameFieldTestCase(APITestCase):

    URL = '/api/v1/game/field/'

    def setUp(self):
        self.john = John.create()
        self.john_gamer = Gamer(self.john)

    def test_url_exists_at_desired_location(self):
        resp = self.client.get(self.URL)

        self.assertNotEqual(
            resp.status_code,
            status.HTTP_404_NOT_FOUND,
            "URL doesn't exist at desired location!"
        )

    def test_url_can_be_reversed(self):
        try:
            reverse('api-v1:game:field')
        except NoReverseMatch:
            self.fail("Can't reverse the url for GameField!")


    def test_auth_user_access_permitted(self):
        self.client.force_login(self.john)
        resp = self.client.get(self.URL)

        self.assertNotEqual(
            resp.status_code,
            status.HTTP_403_FORBIDDEN,
            "Authenticated user has no access to GameField!"
        )

    def test_not_auth_user_access_denied(self):
        resp = self.client.get(self.URL)

        self.assertEqual(
            resp.status_code,
            status.HTTP_403_FORBIDDEN,
            "Not auth user has access to GameField!"
        )

    def test_get(self):
        """
        Test get game field via API.
        """
        john_gamer = Gamer(self.john)
        john_gamer.gamer.set_new_location(50, 50)
        john_gamer.tasks.start(1)

        # in game field, in game, 2 tasks started:
        user_1 = ActiveUser.create()
        gamer_1 = Gamer(user_1)
        gamer_1.gamer.set_new_location(45, 40)
        gamer_1.tasks.start(1)
        gamer_1.tasks.start(2)

        # in game field, in game, 1 task started:
        user_2 = ActiveUser.create()
        gamer_2 = Gamer(user_2)
        gamer_2.gamer.set_new_location(55, 60)
        gamer_2.tasks.start(3)

        self.client.force_login(self.john)

        resp = self.client.get(self.URL)

        with self.subTest("Test status is correct"):
            self.assertEqual(
                resp.status_code, status.HTTP_200_OK,
            )

        with self.subTest("Test response is not empty"):
            # as we tested 'show_game_field' method in details, here we run smoke test only:
            self.assertNotEqual(
                resp.json(),
                []
            )