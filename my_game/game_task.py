from random import randint
from collections import namedtuple

from django.core.cache import cache as redis

from .models import Gamer


class GameTaskDuration:
    MIN = 10
    MAX = 10 * 60  # 10 minutes

    @staticmethod
    def random_duration():
        """
        Calculate random duration in seconds.
        """
        return randint(GameTaskDuration.MIN, GameTaskDuration.MAX)


class TaskAlreadyRunningError(Exception):
    """
    Raise when a gamer attempt to start the task that is yet running.
    """
    pass


class GameTaskType:
    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3
    TYPE_4 = 4
    TYPES = (TYPE_1, TYPE_2, TYPE_3, TYPE_4)


class GameTaskManager:

    # Fixme: add validation for task_type
    # Fixme: add logging for public methods

    def __init__(self, gamer: Gamer):
        self.gamer = gamer

    def start(self, task_type: int) -> bool:
        """
        Start the task.

        If task is already running raise TaskAlreadyRunningError.

        :return: True if started successfully
        """
        key = self.build_key(task_type)
        value = 'Task {} running!'.format(task_type)
        ttl = GameTaskDuration.random_duration()

        if redis.get(key) is not None:
            raise TaskAlreadyRunningError(
                "Task `{key}` is already running!".format(key=key)
            )

        resp = redis.set(key, value, timeout=ttl)
        return resp

    def stop(self, task_type: int):
        key = self.build_key(task_type)
        redis.delete(key)

    def get_ttl(self, task_type):
        """
        Calculate time-to-left for the gamer's task.

        Return 0 if time is end of task has not been started
        """

        key = self.build_key(task_type)
        return redis.ttl(key)

    def is_task_active(self, task_type: int) -> bool:
        ttl = self.get_ttl(task_type)
        if ttl == 0:
            return False
        return True

    def build_key(self, task_type: int) -> str:
        """
        Build the Redis key for gamer's task.

        Example:
            x-12-y-155-john-task-3
        Where
            12 - gamers location x on the game grid
            155 - gamer's location y on the game grid
            john - gamer's username
            3 - task type

        Note:
            Hyphen '-' isn't allowed to be used as Django username and won't
            be allowed in the future, so the given format is safe.
            See https://code.djangoproject.com/ticket/722
        """
        stringified_args = map(str, [
            'x',
            self.gamer.location_x,
            'y',
            self.gamer.location_y,
            self.gamer.user.username,
            'task',
            task_type,
        ])
        return '-'.join(stringified_args)

    def _parse_key(self, key: str) -> namedtuple:
        """
        Extract location_x, location_y, username, task_type from the given string.
        """
        parsed_str = namedtuple('parsed_str', [
            'location_x',
            'location_y',
            'username',
            'task_type',
        ])

        split_str = key.split("-")

        return parsed_str(
            location_x=split_str[1],
            location_y=split_str[3],
            username=split_str[4],
            task_type=split_str[-1],
        )







