from plone import api

from seantis.people import (
    behaviors,
    interfaces,
    tests
)


class TestSetup(tests.IntegrationTestCase):

    def is_behavior_assignable(self, behavior, interface, factory):

        # use a throwaway type with the given behavior
        new_type = self.new_temporary_type(behaviors=[behavior])

        # create an object of said type
        with self.user('admin'):
            obj = api.content.create(
                id=new_type.id,
                type=new_type.id,
                container=self.new_temporary_folder()
            )

        # adapt the behavior's interface
        adapted = interface(obj)

        # ensure that an instance of the factory is the result
        self.assertIs(type(adapted), factory)
        self.assertIs(adapted.context, obj)

    def test_person_behavior_assignable(self):
        self.is_behavior_assignable(
            interfaces.IPerson.__identifier__,
            interfaces.IPerson,
            behaviors.Person
        )
