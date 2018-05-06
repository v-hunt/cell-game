from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
import factory


User = get_user_model()


class BaseUserFactory(DjangoModelFactory):

    class Meta:
        model = User

    is_staff = False
    is_active = True
    password = 'secret'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Use `create_user` manager method instead of default `create`
        """
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class John(BaseUserFactory):
    """
    John is a regular active registered user.
    """
    first_name = 'John'
    last_name = 'Connor'
    username = 'john_connor'
    email = 'john@test.com'


class Sarah(BaseUserFactory):
    """
    Sarah is another regular active registered user.
    """
    first_name = 'Sarah'
    last_name = 'Connor'
    username = 'sarah_connor'
    email = 'sarah@test.com'

class ActiveUser(BaseUserFactory):
    first_name = factory.Sequence(lambda n: 'FirstName #{}'.format(n + 1))
    last_name = factory.Sequence(lambda n: 'LastName #{}'.format(n + 1))
    username = factory.Sequence(lambda n: 'user_{}'.format(n + 1))
    email = factory.Sequence(lambda n: 'user_{}@test.com'.format(n + 1))
