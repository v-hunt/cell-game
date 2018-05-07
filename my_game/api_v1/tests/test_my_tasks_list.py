from unittest import mock

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.urls.exceptions import NoReverseMatch

from base.tests.factories import John
from my_game.gamer import Gamer


@mock.patch("my_game.game_task.GameTaskDuration.random_duration", mock.MagicMock(return_value=42))
class MyTasksListTestCase(APITestCase):

    URL = '/api/v1/game/my-tasks/'

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
            reverse('api-v1:game:task-list')
        except NoReverseMatch:
            self.fail("Can't reverse the url for MyTasksList!")


    def test_auth_user_access_permitted(self):
        self.client.force_login(self.john)
        resp = self.client.get(self.URL)

        self.assertNotEqual(
            resp.status_code,
            status.HTTP_403_FORBIDDEN,
            "Authenticated user has no access to MyTasksList!"
        )

    def test_not_auth_user_access_denied(self):
        resp = self.client.get(self.URL)

        self.assertEqual(
            resp.status_code,
            status.HTTP_403_FORBIDDEN,
            "Not auth user has access to MyTasksList!"
        )

    def test_post(self):
        """
        Test create game task via API.
        """
        self.client.force_login(self.john)

        with self.subTest("Test start task success"):
            resp = self.client.post(self.URL, data={'taskType': 1})

            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Gamer cant create the task via API!"
            )

        with self.subTest("Start the same task again fail"):
            resp = self.client.post(self.URL, data={'taskType': 1})

            self.assertEqual(
                resp.status_code,
                status.HTTP_409_CONFLICT
            )

    def test_get(self):
        """
        Test get list of user's running game tasks.
        """
        task_types = [1, 2]

        for task_type in task_types:
            self.john_gamer.tasks.start(task_type)

        self.client.force_login(self.john)
        resp = self.client.get(self.URL)

        self.assertListEqual(
            resp.json(),
            ['Type: 1, time left: 42s', 'Type: 2, time left: 42s'],
            "Gamer can't get list of task via API!"
        )




