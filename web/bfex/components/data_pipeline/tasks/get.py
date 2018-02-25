from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import Faculty
from bfex.common.exceptions import WorkflowException


class GetFacultyFromElasticSearch(Task):
    """
    Gets all Faculty Members data from elastic.
    """
    def __init__(self):
        self.task_name = "Get all Faculty Members"

    def is_requirement_satisfied(self, data):
        satisfied = True
        
        return satisfied

    def run(self, data):
        print("get faculty elastic")
        s = Faculty.search()
        allFaculty = [faculty for faculty in s.scan()]
        print(allFaculty)
        return allFaculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()
