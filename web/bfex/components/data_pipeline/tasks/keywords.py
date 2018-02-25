from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import Keywords
from bfex.common.exceptions import WorkflowException

class UpdateKeywordsFromScrape(Task):
    """
    Updates Keywords of a Faculty Members data in elastic.
    """
    def __init__(self):
        self.task_name = "Update Keywords From Scrape"

    def is_requirement_satisfied(self, data):
        satisfied = True

        if (not isinstance(data, tuple) or
                not isinstance(data[0], str) or
                not isinstance(data[1], Scrapp)):
            satisfied = False

        return satisfied


    def run(self,data):
        professor_id = data[0]
        scrapp = data[1]

        search_results = Keywords.search().query('match', id=professor_id).execute()
        if len(search_results) > 1:
            # Shouldn't happen, but could.
            raise WorkflowException("Professor id is ambiguous during search... More than 1 result")

        keywords = search_results[0]

        if "text" in scrapp.meta_data:
            keywords.rake_keyword = scrapp.meta_data["text"]

        keywords.save()

        return keywords


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Keywords.init()

    search = Keywords.search()
    results = search.query('match', id="370")

    for keywords in results:
        print(keywords)
