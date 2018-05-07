# Sample game server written in Django and DRF

## How to start

This is a Django project, so starting is a usual Django routine:

```
# install requirements:
pip install -r requirements.txt

# run migrations:
./manage.py migrate

# run tests:
./manage.py test
```

You need to install and run Redis:
```
redis-server
```

When Redis is running, you can initialyze the game:

```
./manage.py init_game
```

Wait for some time... It is gonna create 20k users and start game tasks for them

After that you can run the server:

```
./manage.py runserver
```


## REST API
Allows user to leverage their tasks on the server and get information about the game.
Pay attention, that all endpoints require authentication.

#### GET /api/v1/game/my-tasks/
Get informattion about all user's running tasks.

#### POST /api/v1/game/my-tasks/
Params: taskType - int from 1 to 4
Start the task on the server.

#### DEL /api/v1/game/my-tasks/3/
Stop the game task of type 3


#### GET /api/v1/game/field/
Get information about gamers field.
Return all gamers and their running tasks in the area of size 33x33

