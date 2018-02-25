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

        search_results = Faculty.search().query().execute()
        #if len(search_results) > 1:
            # Shouldn't happen, but could.
        #   raise WorkflowException("Faculty name is ambiguous during search... More than 1 result")
        print(search_results)
        # faculty = search_results[0]

        # if "orcid_link" in scrapp.meta_data:
        #     faculty.orc_id = scrapp.meta_data["orcid_link"]

        # if "researchid_link" in scrapp.meta_data:
        #     faculty.research_id = scrapp.meta_data["researchid_link"]

        # faculty.save()

        return search_results


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()

    # search = Faculty.search()
    # results = search.query('match', name="Neil.Adames")

    # for faculty in results:
    #     print(faculty)
