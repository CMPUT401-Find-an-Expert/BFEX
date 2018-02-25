from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import Faculty
from bfex.common.exceptions import WorkflowException


class UpdateFacultyFromScrape(Task):
    """
    Updates a Faculty Members data in elastic, given a scrape of that faculty members directory page.
    """
    def __init__(self):
        self.task_name = "Update Faculty From Scrape"

    def is_requirement_satisfied(self, data):
        satisfied = True

        if (not isinstance(data, tuple) or
                not isinstance(data[0], str) or
                not isinstance(data[1], Scrapp)):
            satisfied = False

        return satisfied

    def run(self, data):
        faculty_name = data[0]
        scrapp = data[1]
    
        search_results = Faculty.search().query('match', name=faculty_name).execute()
        if len(search_results) > 1:
            # Shouldn't happen, but could.
            raise WorkflowException("Faculty name is ambiguous during search... More than 1 result")

        faculty = search_results[0]

        if "orcid_link" in scrapp.meta_data:
            faculty.orc_id = scrapp.meta_data["orcid_link"]

        if "researchid_link" in scrapp.meta_data:
            faculty.research_id = scrapp.meta_data["researchid_link"]
    
        faculty.save()

        return faculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()

    search = Faculty.search()
    results = search.query('match', name="Neil.Adames")

    for faculty in results:
        print(faculty)
