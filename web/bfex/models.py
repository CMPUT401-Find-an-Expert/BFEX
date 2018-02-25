from elasticsearch_dsl import DocType, Integer, Text
from elasticsearch import NotFoundError


class Model(object):
    """Basic class that provides utility methods to our elasticsearch models."""

    @classmethod
    def safe_get(cls, id):
        """Performs a safe get of an elasticsearch object by id, avoiding 404 exception from elasticsearch.

        :param id: The id of the object in elastic to get.
        :return The object if found, otherwise None."""
        try:
            obj = cls.get(id=id)
        except NotFoundError:
            obj = None
        return obj


class Faculty(DocType, Model):
    """Definition of the basic Faculty doctype.

    Contains any information related to a Faculty member instance pulled from the Forum data dump, or page scrapes.
    Data is saved in the elaticsearch index faculty.
    """
    faculty_id = Integer(required=True)
    name = Text(required=True)
    email = Text(required=True)
    department = Text()

    google_scholar = Text()
    orc_id = Text()
    sciverse_id = Text()
    research_id = Text()

    user_keywords = Text()

    class Meta:
        index = "faculty"

    def __str__(self):
        return "<Faculty ID:{} Name: {} Email: {}".format(self.faculty_id, self.name, self.email)

class Keywords(DocType,Model):
    id = Integer(required=True)
    rake_keywords = Text()

    class Mata: 
        index = "keywords"

class Grant(DocType):
    """Definition of the basic Grant doctype.

    Contains any information related to a Grant instance pulled from the Forum data dump, or page scrapes.
    Data is saved in the elaticsearch index grants.
    """
    faculty_id = Integer(required=True)
    grant_id = Integer()                    # grant_id is the provided id in the json data dump. May not be useful.

    application_title = Text()
    application_area_group = Text()
    application_area = Text()
    research_subject = Text()

    co_applicants = Integer()

    class Meta:
        index = "grants"


class Publication(DocType):
    """Definition of the basic Publication doctype.

    Contains any information related to a Publication instance pulled from the Forum data dump, or page scrapes.
    Data is saved in the elaticsearch index grants.
    """
    publication_id = Integer(required=True)
    authors = Integer(required=True)
    title = Text()
    type = Text()
    url = Text()
    data = Text()
    
    class Meta:
        index = "publications"


def initialize_models():
    """Initializes the mappings of all models in ElasticSearch. Expects that a connection to elastic has already been
    initialized.
    """
    Faculty.init()
    Grant.init()
    Publication.init()


# if __name__ == "__main__":
#     from elasticsearch_dsl.connections import connections
#     connections.create_connection(hosts=["localhost"])

#     Faculty.init()

#     prof = Faculty(meta={'id': 42}, name="Garry Bullock", email="gbullock@ualberta.ca", faculty_id=42)
#     prof.save()

#     saved_prof = Faculty.get(id=42)
#     print(saved_prof.name)

#     print(connections.get_connection().cluster.health())