# Generated by Django 2.0.4 on 2018-05-05 23:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import my_game.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gamer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_x', models.PositiveSmallIntegerField(default=my_game.models.GameGrid.random_x, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(512)])),
                ('location_y', models.PositiveSmallIntegerField(default=my_game.models.GameGrid.random_y, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(512)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gamer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='gamer',
            unique_together={('user', 'location_x', 'location_y')},
        ),
    ]