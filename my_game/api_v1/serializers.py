from rest_framework import serializers as srlz

from my_game.game_task import GameTaskType


class TaskTypeSerializer(srlz.Serializer):
    taskType = srlz.ChoiceField(choices=GameTaskType.TYPES)
