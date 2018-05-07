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
You can try each of the urls in your browser.


#### GET /api/v1/game/my-tasks/
Get informattion about all user's running tasks.

#### POST /api/v1/game/my-tasks/
*Params:* taskType - int from 1 to 4
Start the task on the server.

#### DEL /api/v1/game/my-tasks/3/
Stop the game task of type 3


#### GET /api/v1/game/field/
Get information about gamers field.
Return all gamers and their running tasks in the area of size 33x33


## Authentication

Use `/api/v1/auth/login/` for login and `/api/v1/auth/logout/` for logout.

For automatically created user you can use the following credential:

- **username:** user_5
- **email:** user_5@example.com
- **password:** qwerty

`5` here is an user number





