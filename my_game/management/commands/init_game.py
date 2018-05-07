from random import sample, randrange

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from my_game.gamer import Gamer
from my_game.game_task import GameTaskType


User = get_user_model()


class Command(BaseCommand):
    help = 'Fill game board by gamers and run game tasks'

    NUM_OF_GAMERS = 20000

    def handle(self, *args, **options):

        for num in range(self.NUM_OF_GAMERS):
            username = "user_{}".format(num)
            email = username + '@example.com'
            password = 'qwerty'

            user = self._get_or_create_user(username, email, password)

            gamer = Gamer(user)

            if not gamer.in_game():
                task_types = self._get_random_task_types()

                for task_type in task_types:
                    gamer.tasks.start(task_type)

                self.stdout.write(
                    self.style.SUCCESS(
                        "{} started game tasks: {}".format(
                            username, task_types,
                        )
                    )
                )


        print()
        self.stdout.write(
            self.style.SUCCESS('\tGame initialized successfully!')
        )

    def _get_or_create_user(self, username, email, password):
        try:
            user = User.objects.create_user(username, email, password)

            self.stdout.write(
                self.style.SUCCESS("Create user: {}".format(username)))

        except IntegrityError:
            user = User.objects.get(username=username)

            self.stdout.write(
                self.style.SUCCESS("Get existed user: {}".format(username)))

        return user

    @staticmethod
    def _get_random_task_types():
        task_types_all = GameTaskType.TYPES
        return sample(
            population=task_types_all,
            k=randrange(len(task_types_all))
        )