from bfex.components.data_pipeline.tasks import Task
from bfex.common.exceptions import WorkflowTaskArgumentException


class Workflow(object):

    def __init__(self, tasks, init_data=None):
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
        return self.tasks[self.current_step]

    def run_next(self):
        if self.current_step >= self.steps:
            return False                        # ? This doesn't seem like a great approach to tell the workflow to stop

        current_task = self.get_current_task()()    # Fetch the class of the next task, and instantiate it

        if current_task.is_requirement_satisfied(self.last_result):
            result = current_task.run(self.last_result)
            self.last_result = result
            self.current_step += 1
        else:
            raise WorkflowTaskArgumentException("{} received an unsatisfactory argument - {}")

        return True

    def run(self):
        is_finished = False

        while not is_finished:
            is_finished = not self.run_next()

        return self.last_result


if __name__ == "__main__":
    from bfex.components.data_pipeline.tasks import FacultyPageScrape, UpdateFacultyFromScrape
    from elasticsearch_dsl import connections
    connections.create_connection()

    tasks = [FacultyPageScrape, UpdateFacultyFromScrape]

    workflow_manager = Workflow(tasks, "William.Allison")

    result = workflow_manager.run()

    print(result)
