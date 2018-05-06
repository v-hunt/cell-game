from django.test import TestCase
from django_redis import get_redis_connection
from django.core.cache import cache as redis

from base.tests.factories import John
from my_game.game_task import (
    GameTaskDuration,
    TaskAlreadyRunningError,
    GameTaskType,
    GameTaskManager,
)
from my_game.models import Gamer


class GameTaskManagerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.john = John.create()
        cls.location_x = 5
        cls.location_y = 10
        cls.john_gamer = Gamer.objects.create(
            user=cls.john,
            location_x=cls.location_x,
            location_y=cls.location_y,
        )
        cls.task_manager = GameTaskManager(gamer=cls.john_gamer)

    def tearDown(self):
        get_redis_connection("default").flushall()

    def test_build_key(self):
        self.assertEqual(
            self.task_manager.build_key(4),
            'x-5-y-10-john_connor-task-4',
            '`key` is constructed not properly!'
        )

    def test_start(self):

        with self.subTest("Test start new task"):
            task_type = 4
            self.task_manager.start(task_type)
            key = self.task_manager.build_key(task_type)

            self.assertIsNotNone(
                redis.get(key),
                "Can't start new task!"
            )

        with self.subTest("Test can't start already running task"):
            with self.assertRaises(TaskAlreadyRunningError):
                self.task_manager.start(task_type)

    def test_stop(self):
        task_type = 4
        self.task_manager.start(task_type)
        key = self.task_manager.build_key(task_type)

        self.task_manager.stop(task_type)

        self.assertIsNone(
            redis.get(key),
            "Gamer can't stop the task!"
        )

    def test_get_ttl(self):
        task_type = 4
        self.task_manager.start(task_type)

        self.assertGreater(
            self.task_manager.get_ttl(task_type), 0,
            "`get_ttl` method isn't working!"
        )