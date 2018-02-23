from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self, task_name):
        self.task_name = task_name

    def is_requirement_satisfied(self, data):
        """ Method used to tell if this task is able to run on the given data.

        This default implementation returns true, no matter what is passed to it. It should be overridden if the
        task has some validation or strict requirements on what can be passed into.
        :param data:
        :return:
        """
        return True

    @abstractmethod
    def run(self, data):
        pass

    def __str__(self):
        return "<Task: {}>".format(self.task_name)
