import pytest

from bfex.components.data_pipeline import workflow, tasks
from bfex.common.exceptions import WorkflowTaskArgumentException


class TestWorkflow(object):

    class SimpleTask(tasks.Task):
        """Define a simple task that we can use for testing the workflow. Simply adds one to the given data."""
        def __init__(self):
            super().__init__("Add One Task")

        def is_requirement_satisfied(self, data):
            if isinstance(data, int):
                return True
            return False

        def run(self, data):
            return data + 1

    def test_basic_complete_workflow(self):
        task_list = [self.SimpleTask, self.SimpleTask]

        workflow_manager = workflow.Workflow(task_list, init_data=0)

        result = workflow_manager.run()

        assert result == 2

    def test_basic_workflow_steps(self):
        task_list = [self.SimpleTask, self.SimpleTask]

        workflow_manager = workflow.Workflow(task_list, init_data=0)
        assert workflow_manager.current_step == 0
        assert workflow_manager.steps == 2
        assert workflow_manager.last_result == 0

        is_not_finished = workflow_manager.run_next()
        assert workflow_manager.current_step == 1
        assert workflow_manager.last_result == 1
        assert is_not_finished

        is_not_finished = workflow_manager.run_next()
        assert workflow_manager.current_step == 2
        assert workflow_manager.last_result == 2
        assert is_not_finished

        is_not_finished = workflow_manager.run_next()
        assert workflow_manager.last_result == 2
        assert not is_not_finished

    def test_workflow_exceptions(self):
        # Test a ValueError is raised when creating a workflow with no tasks in the tasklist
        task_list = []
        with pytest.raises(ValueError):
            workflow.Workflow(task_list)

        # Test that a TypeError is raised when creating a workflow using a tasklist that does not contain only tasks.
        task_list = ["data", "another data"]
        with pytest.raises(TypeError):
            workflow.Workflow(task_list)

        task_list = [self.SimpleTask, "data", self.SimpleTask]
        with pytest.raises(TypeError):
            workflow.Workflow(task_list)

        # Test that a WorkflowArgumentException is raised when incorrect data is passed to a task
        task_list = [self.SimpleTask]
        workflow_manager = workflow.Workflow(task_list, init_data="bad data")
        with pytest.raises(WorkflowTaskArgumentException):
            workflow_manager.run()

