from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import Faculty
from bfex.common.exceptions import WorkflowException
from bfex.components.key_generation.rake_approach import *



class UpdateFacultyFromScrape(Task):
    """Updates a Faculty Members data in elastic, given a scrape of that faculty members directory page."""

    def __init__(self):
        self.task_name = "Update Faculty From Scrape"

    def is_requirement_satisfied(self, data):
        """Verifies that the data is acceptable for submitting into elasticsearch.

        :param data: Expected to be a tuple of the form <str, Scrapp>, containing the faculty members name as found in
                    elasticsearch, and the Scrapp produced by scraping their page.
        :returns True if the data is of the form above, else False.
        """
        satisfied = True
        
        for faculty in data:
            if (not isinstance(faculty, tuple) or
                    not isinstance(faculty[0], str) or
                    not isinstance(faculty[1], Scrapp)):
                satisfied = False

        return satisfied

    def run(self, data):
        """Updates a Faculty members information in Elasticsearch, based on the result of a scrape.

        :param data: list of tuples of form <str, Scrapp>
        :return: The updated instance of a Faculty model.
        """
        for faculty in data:
            faculty_name = faculty[0]
            scrapp = faculty[1]


            search_results = Faculty.search().query('match', name=faculty_name).execute()
            if len(search_results) > 1:
                # Shouldn't happen, but could.
                raise WorkflowException("Faculty name is ambiguous during search... More than 1 result")

            faculty = search_results[0]

            if "orcid_link" in scrapp.meta_data:
                faculty.orc_id = scrapp.meta_data["orcid_link"]

            if "researchid_link" in scrapp.meta_data:
                faculty.research_id = scrapp.meta_data["researchid_link"]

            if "text" in scrapp.meta_data:
                 faculty.text = scrapp.meta_data["text"]

            faculty.save()

        return faculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()

    search = Faculty.search()
    results = search.query('match', name="Erin.Bayne")

    for faculty in results:
        print(faculty)
