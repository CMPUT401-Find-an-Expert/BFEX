from bfex.components.data_pipeline.tasks import Task
from bfex.common.exceptions import WorkflowTaskArgumentException


class Workflow(object):
    """A workflow is a series of tasks to be run in sequence.

    Each task is verified prior to running, by calling the is_requirement_satisfied method of the task. It will only
    be run if that method returns true. The result of each step is stored in last_result, and can be accessed if needed.
    """

    def __init__(self, tasks, init_data=None):
        """Creates a new workflow with the passed in series of tasks.

        :param list tasks: A list of Task class references to be instantiated and run.
        :param init_data: Any initialization data that should be fed into the first task.
        :exception ValueError: If the tasks list is empty
        :exception TypeError: If any of the class references in tasks are not a subclass of Task
        """
        self.tasks = tasks
        self.steps = len(tasks)
        self.current_step = 0
        self.last_result = init_data

        # TODO: It would be cool to support dynamic loading of classes at runtime. So we could specify a workflow
        # as a list of string names of the tasks. You could define new workflows from an api that way.
        if self.steps < 1:
            raise ValueError("A workflow must contain at least one step.")

        for task in tasks:
            if not issubclass(task, Task):
                raise TypeError("A workflow must be made up of only of references to Task classes.")

    def get_current_task(self):
        """Returns the next task to be run."""
        return self.tasks[self.current_step]

    def get_last_result(self):
        """Returns the result of the previously ran task."""
        return self.last_result

    def run_next(self):
        """Runs the next task in the workflow.

        :exception WorkflowTaskArgumentException: If a task receives unsatisfactory data.
        :returns False if there are no more steps to be run, True if the step succeeds.
        """
        if self.current_step >= self.steps:
            return False                        # ? This doesn't seem like a great approach to tell the workflow to stop

        current_task = self.get_current_task()()    # Fetch the class of the next task, and instantiate it
        # print(self.last_result)
        if current_task.is_requirement_satisfied(self.last_result):
            result = current_task.run(self.last_result)
            self.last_result = result
            self.current_step += 1
        #else:
            #raise WorkflowTaskArgumentException("{} received an unsatisfactory argument - {}")

        return True

    def run(self):
        """Runs the entire workflow, from the current step to finish.

        :returns The result of the final task.
        """
        is_finished = False

        while not is_finished:
            is_finished = not self.run_next()

        return self.last_result


if __name__ == "__main__":
    from bfex.components.data_pipeline.tasks import FacultyPageScrape, UpdateFacultyFromScrape, GetFacultyFromElasticSearch
    from elasticsearch_dsl import connections
    connections.create_connection()

    tasks = [GetFacultyFromElasticSearch,FacultyPageScrape,UpdateFacultyFromScrape]
    workflow_manager = Workflow(tasks, "Stan.Boutin")
    # workflow_manager = Workflow(tasks, "thing")

    result = workflow_manager.run()

    print('result',result)
