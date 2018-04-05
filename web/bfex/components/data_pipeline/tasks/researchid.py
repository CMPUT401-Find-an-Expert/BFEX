from datetime import datetime
from bfex.components.scraper.scraper_factory import ScraperFactory
from bfex.components.scraper.scraper_type import ScraperType
from bfex.models import Faculty, Document, Keywords
from bfex.common.utils import URLs, FacultyNames
from bfex.common.exceptions import WorkflowException, ScraperException
from bfex.components.data_pipeline.tasks.task import Task
from bfex.components.key_generation.rake_approach import *


class ResearchIdPageScrape(Task):
    def __init__(self):
        super().__init__("ResearchId Page Scrape")

    def is_requirement_satisfied(self, data):
        """ Checks the requirements for a faculty page scraping are satisfied.

        For a ResearchId page scrape, we get the links from ElasticSearch.
        :param list data: list of all faculty
        :return: True if valid data, otherwise false
        """

        return isinstance(data, Faculty)

    def run(self, data):

        """Performs a scraping of a faculty members ResearchId page.
        :param data is a faculty object
        :return: last faculty member handled
        """
        
        faculty = data
        if isinstance(faculty, str):
            search_results = Faculty.search().query('match', name=faculty).execute()
            if len(search_results) > 1:
                # Shouldn't happen, but could.
                raise WorkflowException("Professor id is ambiguous during search ... More than 1 result")
            faculty = search_results[0]
            
        faculty_name = faculty.name

        
        Document.search().query('match', faculty_id=faculty.faculty_id) \
            .query("match", source="ResearchId") \
            .delete()

        print("Running researchid scrape on {}. Research id {}."
                .format(faculty_name, faculty.research_id))

        if faculty.research_id is not None:
            
            scraper = ScraperFactory.create_scraper(faculty.research_id, ScraperType.RESEARCHID)
            try:
                scrapps = scraper.get_scrapps()
            except ScraperException:
                return faculty

            keywords_and_description = scrapps[0]
            titles = scrapps[1:]

            doc = Document()
            doc.faculty_id = faculty.faculty_id
            doc.source = "ResearchId"

            keywords = Keywords()
            keywords.faculty_id = faculty.faculty_id
            keywords.datasource = "user_keywords"
            keywords.approach_id  = "4"

            try:
                doc.text = keywords_and_description.meta_data["description"]
            except:
                print("No description")
                doc.text = ""
            try:
                doc.user_keywords = keywords_and_description.meta_data["keywords"]
                keywords.keywords = keywords_and_description.meta_data["keywords"]
            except:
                print("No keywords")
            doc.date = datetime.now()
            doc.save()
            keywords.save()
            
            for scrapp in titles:
                doc = Document()
                doc.source = "ResearchId"
                doc.faculty_id = faculty.faculty_id
                doc.text = scrapp.title
                doc.date = datetime.now()
                doc.save()

        return faculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()
    Document.init()