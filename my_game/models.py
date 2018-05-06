import datetime as dt
from random import randint, randrange

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.contrib.auth import get_user_model


class GameGrid:
    MAX_X = 512
    MAX_Y = 512

    @staticmethod
    def random_x():
        return randrange(GameGrid.MAX_X)

    @staticmethod
    def random_y():
        return randrange(GameGrid.MAX_Y)

    @staticmethod
    def random_location():
        """
        Return random coordinate on the game grid.
        """
        return GameGrid.random_x(), GameGrid.random_y()


class Gamer(models.Model):
    """
    NOTE:
    This class is intended for persistence mostly.
    If you want to leverage business logic of the gamer,
    use 'my_game.gamer.Gamer' class for it.
    """
    user = models.OneToOneField(
        get_user_model(),
        related_name='gamer',
        on_delete=models.CASCADE,
    )


    # we use MinValueValidator(0) as Django ORM doesn't support the constraint (value >=0) for SQLite:
    location_x = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(GameGrid.MAX_X),
        ),
        default=GameGrid.random_x,
    )
    location_y = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(GameGrid.MAX_Y),
        ),
        default=GameGrid.random_y,
    )

    class Meta:
        # that's impossible to have two gamers in the same location
        unique_together = ('user', 'location_x', 'location_y')

    @classmethod
    def from_user(cls, user):
        """
        Initialize Gamer from regular User.
        """
        return Gamer.objects.get(user=user)
