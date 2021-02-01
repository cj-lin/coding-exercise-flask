import factory
from myapi.models import Task, User


class TaskFactory(factory.Factory):

    name = factory.Sequence(lambda n: "task%d" % n)

    class Meta:
        model = Task

class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User
