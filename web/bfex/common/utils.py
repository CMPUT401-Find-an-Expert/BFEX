import re


def generate_names_from_json(item):
    name_from_json = item['name']
    name_from_json = re.sub('[.]', '', name_from_json)
    name_list = re.findall('[A-Z][^A-Z]*', name_from_json)
    formated_name = "-".join(name_list).lower()
    return formated_name


class URLs:
    """Utilities for working with urls"""
    FACULTY_DIRECTORY = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

    @staticmethod
    def build_faculty_url(name):
        """Builds a faculty directory url from a Faculty name"""
        url_safe_name = FacultyNames.build_url_name(name)

        return URLs.FACULTY_DIRECTORY + url_safe_name


class FacultyNames:
    """Utilities for working with Faculty names."""
    name_regex = re.compile(r'\w+\.\w+')
    split_regex = re.compile(r'(?!^)([A-Z][a-z]+)')

    @staticmethod
    def validate_name(name):
        """Validates that a faculty name is of the form First.Last"""
        if FacultyNames.name_regex.match(name):
            return True
        return False

    @staticmethod
    def build_url_name(name):
        """Builds the url safe name expected for faculty directory urls, of the form first-middle-last"""
        name_list = FacultyNames.split_regex.sub(r' \1', name).replace(r'.', r'').split()

        url_safe = '-'.join(name_list)

        return url_safe.lower()


if __name__ == "__main__":
    print(FacultyNames.build_url_name("JNelson.Amaral"))