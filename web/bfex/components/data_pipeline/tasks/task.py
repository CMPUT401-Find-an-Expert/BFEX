from abc import ABC, abstractmethod


class Task(ABC):
    """Task is a basic definition of a unit of work to be performed.

    It is an abstract base class that cannot be instantiated on its own. Instead, implementations should be defined
    and used.
    """

    def __init__(self, task_name):
        """Creates a new Task, with the given name.

        Name should be used for information purposes such as logging, or printing."""
        self.task_name = task_name

    def is_requirement_satisfied(self, data):
        """Method used to tell if this task is able to run on the given data.

        This default implementation returns true, no matter what is passed to it. It should be overridden if the
        task has some validation or strict requirements on what can be passed into.
        :param data: The data that will be run in the task.
        :returns True if the data is valid for this task, false if otherwise.
        """
        return True

    @abstractmethod
    def run(self, data):
        """The body of a task. It defines the actual work that should be done by this task.

        :param data: Data to run this task on.
        :return: The result of the task.
        """
        pass

    def __str__(self):
        return "<Task: {}>".format(self.task_name)
