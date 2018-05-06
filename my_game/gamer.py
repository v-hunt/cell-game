from .models import Gamer as GamerModel, GameGrid
from .game_task import GameTaskType, GameTaskManager


class Gamer:
    """
    Initialize a gamer and provide him with common tasks operations.
    """

    GAME_FIELD_SIZE = 33

    def __init__(self, user):
        self.gamer = Gamer._setup_gamer(user)
        self.task_manager = GameTaskManager(self.gamer)

    @staticmethod
    def _setup_gamer(user) -> GamerModel:
        """
        Start or continue the game (i.e. assign self.gamer).

        User starts the game when he created the Game instance at the first time.
        User continue the game when user.gamer is already exists. In this case
        we give him new position on the GameGrid if he doesn't have running tasks.
        """
        if not hasattr(user, 'gamer'):  # <- check if user is a gamer
            gamer = GamerModel.objects.create(user=user)

        else:
            gamer = GamerModel.from_user(user)

            if not GameTaskManager(gamer).running_tasks():
                gamer.set_new_location()

        return gamer

    def in_game(self) -> bool:
        """
        When gamer has running tasks we consider him as active.
        """
        return self.task_manager.running_tasks()


