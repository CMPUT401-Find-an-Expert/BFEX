import pytest

from bfex.common.utils import *


class TestFacultyNames(object):
    def test_validate_name(self):
        valid_name = "JNelson.Amaral"
        invalid_name = "Nelson Amaral"
        invalid_name_2 = "Nelson, Amaral"

        assert FacultyNames.validate_name(valid_name)
        assert not FacultyNames.validate_name(invalid_name)
        assert not FacultyNames.validate_name(invalid_name_2)

    def test_build_directory_url(self):
        valid_name = "Nelson.Amaral"
        valid_name_2 = "JNelson.Amaral"

        url_name = FacultyNames.build_url_name(valid_name)
        assert url_name.islower()
        assert "-" in url_name
        assert "nelson-amaral"

        url_name = FacultyNames.build_url_name(valid_name_2)
        assert url_name.islower()
        assert "-" in url_name
        assert "j-nelson-amaral"


class TestURLs(object):
    def test_build_faculty_url(self):
        valid_name = "Nelson.Amaral"
        valid_name_2 = "JNelson.Amaral"

        url = URLs.build_faculty_url(valid_name)
        assert URLs.FACULTY_DIRECTORY in url
        assert (url == "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/nelson-amaral")

        url = URLs.build_faculty_url(valid_name_2)
        assert URLs.FACULTY_DIRECTORY in url
        assert (url == "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/j-nelson-amaral")


