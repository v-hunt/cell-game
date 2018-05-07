from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import TaskTypeSerializer
from my_game.gamer import Gamer
from my_game.game_task import TaskAlreadyRunningError


class MyTasksList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        Return gamers all currently running tasks.
        """
        gamer = Gamer(request.user)
        data = gamer.tasks.get_all_task_stringified()
        return Response(data)

    def post(self, request):
        """
        Create new task by a user.
        """
        serializer = TaskTypeSerializer(data=request.data)

        if serializer.is_valid():
            task_type = serializer.validated_data['taskType']
            gamer = Gamer(request.user)

            try:
                ttl = gamer.tasks.start(task_type)
                data = {'taskType': task_type, 'ttl': ttl}
                return Response(data, status=status.HTTP_201_CREATED)
            except TaskAlreadyRunningError as err:
                return Response(
                    {'msg': str(err)},
                    status.HTTP_409_CONFLICT,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTasksDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, task_type):
        """
        Kill gamer's running task.
        """
        gamer = Gamer(request.user)
        gamer.tasks.stop(task_type)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GameField(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get gamer's field.
        """
        gamer = Gamer(request.user)
        data = gamer.show_game_field()
        return Response(data, status=status.HTTP_200_OK)


my_tasks_list_view = MyTasksList.as_view()
my_tasks_detail_view = MyTasksDetail.as_view()
game_field_view = GameField.as_view()