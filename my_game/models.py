from typing import Union
from random import randrange

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import IntegrityError
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

    def __str__(self):
        return "{username} on ({x}, {y})".format(
            username=self.user.username,
            x=self.location_x,
            y=self.location_y,
        )

    def save(self, *args, **kwargs):
        # we always choose new location if the current is already taken by someone:
        while True:
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                self._new_rand_location()

    @classmethod
    def from_user(cls, user):
        """
        Initialize Gamer from regular User.
        """
        return Gamer.objects.get(user=user)

    def set_new_location(self,
                         x: Union[int, None]=None,
                         y: Union[int, None]=None,
                         save: bool=True):
        """
        Set new location for the gamer on the GameGrid.

        If x and y is not provided, random location will be set.

        :return: new coordinates (x, y)
        """

        if x is None and y is None:
            self._new_rand_location()

        else:
            self.location_x = x
            self.location_y = y

        if save is True:
            self.save()

        return self.location_x, self.location_y

    def _new_rand_location(self):
        self.location_x, self.location_y = GameGrid.random_location()
