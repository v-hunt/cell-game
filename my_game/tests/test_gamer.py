from django.test import TestCase
from django_redis import get_redis_connection
from django.core.cache import cache as redis

from base.tests.factories import John, Sarah
from my_game.game_task import (
    GameTaskDuration,
    TaskAlreadyRunningError,
    GameTaskType,
    GameTaskManager,
)
from my_game.models import Gamer as GamerModel
from my_game.gamer import Gamer


class GamerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.john = John.create()
        cls.location_x = 5
        cls.location_y = 10

        cls.sarah = Sarah.create()
        cls.sarah_gamer = GamerModel.objects.create(user=cls.sarah)

    def tearDown(self):
        get_redis_connection("default").flushall()

    def test_in_game(self):
        john_gamer = Gamer(self.john)

        with self.subTest("test False case"):
            self.assertFalse(
                john_gamer.in_game(),
            )

        with self.subTest("test True case"):
            john_gamer.tasks.start(GameTaskType.TYPE_1)

            self.assertTrue(
                john_gamer.in_game()
            )