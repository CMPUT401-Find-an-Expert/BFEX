from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import *
from bfex.common.exceptions import WorkflowException
from bfex.components.key_generation.rake_approach import *
from bfex.components.key_generation.generic_approach import *



class UpdateKeywordsFromScrape(Task):
    """
    Updates Keywords of a Faculty Members data in elastic.
    """
    def __init__(self):
        self.task_name = "Update Keywords From Scrape"

    def is_requirement_satisfied(self, data):
        satisfied = True

        for faculty in data:

            if (not isinstance(faculty, tuple) or
                    not isinstance(faculty[0], str) or
                    not isinstance(faculty[1], Scrapp)):
                satisfied = False

        return satisfied


    def run(self,data):
        no_text_count = 0
        for faculty in data:
            print(faculty.name)
            faculty_name = faculty.name
    
            search_results = Faculty.search().query('match', name=faculty_name).execute()
            if len(search_results) > 1:
                # Shouldn't happen, but could.
                raise WorkflowException("Professor id is ambiguous during search... More than 1 result")
        
            faculty = search_results[0]
            if faculty.text != None:
                
                rake = RakeApproach()
                rake_keyword = rake.generate_keywords(faculty.text)
                faculty.rake_keywords = rake_keyword

                generic = GenericApproach()
                generic_keyword = generic.generate_keywords(faculty.text)
                faculty.generic_keywords = generic_keyword

                faculty.save()
            else:
                no_text_count+=1
        print("NO TEXT COUNT = ", no_text_count)
        return faculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()

    search = Faculty.search()
    allFaculty = [faculty for faculty in search.scan()]
    task = UpdateKeywordsFromScrape()
    task.run(allFaculty)