import re


def generate_names_from_json(item):
    name_from_json = item['name']
    name_from_json = re.sub('[.]', '', name_from_json)
    name_list = re.findall('[A-Z][^A-Z]*', name_from_json)
    formated_name = "-".join(name_list).lower()
    return formated_name


class URLs:

    FACULTY_DIRECTORY = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

    @staticmethod
    def build_faculty_url(name):
        url_safe_name = FacultyNames.build_url_name(name)

        return URLs.FACULTY_DIRECTORY + url_safe_name


class FacultyNames:

    name_regex = re.compile(r'\w+\.\w+')
    split_regex = re.compile(r'(?!^)([A-Z][a-z]+)')

    @staticmethod
    def validate_name(name):
        if FacultyNames.name_regex.match(name):
            return True
        return False

    @staticmethod
    def build_url_name(name):
        name_list = FacultyNames.split_regex.sub(r' \1', name).replace(r'.', r'').split()

        url_safe = '-'.join(name_list)

        return url_safe.lower()


if __name__ == "__main__":
    print(FacultyNames.build_url_name("JNelson.Amaral"))