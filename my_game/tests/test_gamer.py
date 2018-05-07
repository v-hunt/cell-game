from django.test import TestCase
from django_redis import get_redis_connection
from django.core.cache import cache as redis

from base.tests.factories import John, ActiveUser
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

    # def setUp(self):
    #     self.john = John.create()

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

    def test_show_game_field(self):
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

        # in game field, not in game:
        user_3 = ActiveUser.create()
        gamer_3 = Gamer(user_3)
        gamer_3.gamer.set_new_location(51, 52)

        # out of game field, in game, 1 task started:
        user_4 = ActiveUser.create()
        gamer_4 = Gamer(user_4)
        gamer_4.gamer.set_new_location(200, 300)
        gamer_4.tasks.start(1)

        game_field = john_gamer.show_game_field()

        with self.subTest("Test result length"):
            self.assertEqual(
                len(game_field), 2,
                "Wrong length of game field!"
            )

        with self.subTest("Test gamers are correct in result"):
            self.assertEqual(
                game_field[0]['gamer'],
                user_1.username
            )
            self.assertEqual(
                game_field[1]['gamer'],
                user_2.username
            )

        with self.subTest("Test 'tasks' field length in result"):
            self.assertEqual(
                len(game_field[0]['tasks']), 2
            )
            self.assertEqual(
                len(game_field[1]['tasks']), 1
            )

