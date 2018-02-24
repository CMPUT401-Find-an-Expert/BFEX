from bfex.components.scraper.scraper_factory import ScraperFactory
from bfex.components.scraper.scraper_type import ScraperType
from bfex.models import Faculty
from bfex.common.utils import URLs, FacultyNames
from bfex.components.data_pipeline.tasks.task import Task


class FacultyPageScrape(Task):
    """FacultyPageScrape is a task that uses the Scraper to pull data from a professors faculty directory page."""

    def __init__(self):
        super().__init__("Faculty Directory Page Scrape")

    def is_requirement_satisfied(self, data):
        """Checks the requirements for a faculty page scraping are satisfied.

        For a Faculty Directory page scrape, we can get the data in one of 2 ways. Either a faculty member name is
        passed to us, or an instance of a faculty member is passed in.
        :param data: str or Faculty instance.
        :return: True if the name is a valid one, else False
        """

        # Should this return the data as it is expected for running the task?
        if isinstance(data, str):
            # Apply any additional checks or validations that need to occur on the data
            return FacultyNames.validate_name(data)

        if isinstance(data, Faculty):
            return FacultyNames.validate_name(data.name)

    def run(self, data):
        """Performs a scraping of a faculty members directory page.

        :param data: str or Faculty instance.
        :return: tuple of the faculty name and Scrapp produced by scraping the faculty directory page.
        """
        if isinstance(data, str):
            faculty_name = data
        else:
            faculty_name = data.name

        faculty_directory_url = URLs.build_faculty_url(faculty_name)

        scraper = ScraperFactory.create_scraper(faculty_directory_url, ScraperType.PROFILE)
        scrapp = scraper.get_scrapps()[0]

        return faculty_name, scrapp


if __name__ == "__main__":
    task = FacultyPageScrape()

    if task.is_requirement_satisfied("JNelson.Amaral"):
        task.run("JNelson.Amaral")




