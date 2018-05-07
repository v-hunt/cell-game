from .models import Gamer as GamerModel, GameGrid
from .game_task import GameTaskType, GameTaskManager


class Gamer:
    """
    Initialize a gamer and provide him with common tasks operations.
    """

    GAME_FIELD_SIZE = 33

    def __init__(self, user):
        self.gamer = Gamer._setup_gamer(user)
        self.tasks = GameTaskManager(self.gamer)

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
            gamer = user.gamer

            if not GameTaskManager(gamer).running_tasks():
                gamer.set_new_location()

        return gamer

    def in_game(self) -> bool:
        """
        When gamer has running tasks we consider him as active.
        """
        return self.tasks.running_tasks()

    def show_game_field(self):
        """
        Return gamers from the game field of size 33x33 and their running
        tasks in str format.
        """
        half_of_game_field = self.GAME_FIELD_SIZE // 2

        location_x = self.gamer.location_x
        location_y = self.gamer.location_y

        x_border_min = location_x - half_of_game_field if location_x - half_of_game_field >= 0 else 0
        x_border_max = location_x + half_of_game_field if location_x + half_of_game_field <= GameGrid.MAX_X else GameGrid.MAX_X
        y_border_min = location_y - half_of_game_field if location_y - half_of_game_field >= 0 else 0
        y_border_max = location_y + half_of_game_field if location_y + half_of_game_field <= GameGrid.MAX_Y else GameGrid.MAX_Y

        gamers_from_field = GamerModel.objects.filter(
            location_x__gte=x_border_min,
            location_x__lte=x_border_max,
            location_y__gte=y_border_min,
            location_y__lte=y_border_max,
        )

        res = []

        def in_game(gamer):
            return GameTaskManager(gamer).running_tasks()

        for gamer in gamers_from_field:
            if in_game(gamer) and gamer.user != self.gamer.user :
                res.append({
                    'gamer': gamer.user.username,
                    'location': gamer.location_str,
                    'tasks': GameTaskManager(gamer).get_all_task_stringified(),
                })

        return res


